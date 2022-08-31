import typing, warnings, traceback
from queue import Queue
from threading import Thread, get_ident, Lock
from inspect import signature
from PySide6 import QtWidgets, QtCore


class Task:
	def __init__(self, target, lazy=False):
		self.target = target
		self.lazy = lazy


class BackgroundMethod(Thread):
	"""
	A wrapper to execute a function in a background thread.

	Usage:
	```python
	import time

	@formify.tools.BackgroundMethod
	def expensive_calculation(text):
		time.sleep(1)
		print(text)

	expensive_calculation("1")
	expensive_calculation("2")
	expensive_calculation("3")
	print("Hello") # will be printed first

	```

	Output:
	```
	Hello
	1
	2
	3
	```


	"""
	_lazy = False

	def __init__(self, target: typing.Callable, lazy: bool = None, cleanup: typing.Callable = None):
		"""
		Args:
			target: Target method (is executed, when the BackgroundMethod instance is called)
			lazy: A call is skipped, if a newer one is queued.
			cleanup: Runs after the target, if provided.

		Returns:
			BakgroundMethod(typing.Callable): A callable thread, that executes the target with Callable. If a cleanup is provided, this runs afterwards.
		"""
		Thread.__init__(self)
		self.daemon = True
		self.queue = Queue()
		if lazy is None:
			self.lazy = self._lazy
		else:
			self.lazy = lazy
			warnings.warn("The 'lazy' argument is deprecated. Use the LazyBackgroundMethod instead", DeprecationWarning)
		self.target = target
		self.cleanup = cleanup
		self.start()

	def run(self):
		while True:
			task = self.queue.get()
			while task.lazy and not self.queue.empty():
				task = self.queue.get()

			try:
				task.target()
				if self.cleanup:
					self.cleanup()
			except:
				traceback.print_exc()

	def __call__(self, *args, **kwargs):
		"""
		Executes the self.target with the provided *args and **kwargs.
		"""
		if len(signature(self.target).parameters) == 0:
			func = self.target
		else:
			func = lambda: self.target(*args, **kwargs)

		self.queue.put(Task(
			func,
			lazy=self.lazy
		))


class LazyBackgroundMethod(BackgroundMethod):
	"""
	Executes only the latest call. Helpful for updating a plot and wherever else you are only interested in the latest
	result.

	Usage:
	```python
	import time

	@formify.tools.LazyBackgroundMethod
	def expensive_calculation(text):
		time.sleep(1)
		print(text)

	expensive_calculation("1")
	expensive_calculation("2") # will not be executed!
	expensive_calculation("3")
	print("Hello")

	```

	Output:
	```
	Hello
	1
	3
	```
	"""
	_lazy = True


class Signaller(QtCore.QObject):
	signal = QtCore.Signal(str)

	def __init__(self):
		super().__init__()


class MainThreadOperation():
	def __init__(self):
		self.func = None
		self.lock = Lock()
		# we use a signal to make sure redrawing is done in the main Thread
		self._signal = Signaller()
		self._signal.signal.connect(self._execute)
		#print(f"created {get_ident()}")

	def __call__(self, func):
		self.lock.acquire()
		self.func = func
		#print(f"called {get_ident()}")
		self._signal.signal.emit("emitting")

	@QtCore.Slot(str)
	def _execute(self, _):
		try:
			self.func()
			#print(f"done {get_ident()}")
		finally:
			self.lock.release()


_main_thread_operation = MainThreadOperation()


def do_in_ui_thread(func: typing.Callable):
	"""
	Immediately executes `func` in the main thread (UI thread). Useful when interacting with UI elements.

	Usage:
	```python
	textarea = formify.ControlTextarea("Output")

	@formify.tools.BackgroundMethod
	def expensive_calculation(text):
		time.sleep(1)

		def output_text():
			textarea.value += text + "\\n"

		do_in_ui_thread(output_text)

	expensive_calculation(1)
	expensive_calculation(2)
	expensive_calculation(3)
	```
	The textarea should contain:
	```
	1
	2
	3
	```

	Args:
		func: fucntion to be called (without any arguments)

	"""
	_main_thread_operation(func)
