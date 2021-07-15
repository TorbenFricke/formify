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
	def __init__(self, target: typing.Callable, lazy=False, cleanup: typing.Callable = None):
		"""
		A callable thread, that executes the target with Callable. If a cleanup is provided, this runs afterwards.
		:param target: Target method (is executed, when the BackgroundMethod instance is called)
		:param lazy: A call is skipped, if a newer one is queued.
		:param cleanup: Runs after the target, if provided.
		"""
		Thread.__init__(self)
		self.daemon = True
		self.queue = Queue()
		self.lazy = lazy
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

		:param args:
		:param kwargs:
		:return:
		"""
		if len(signature(self.target).parameters) == 0:
			func = self.target
		else:
			func = lambda: self.target(*args, **kwargs)

		self.queue.put(Task(
			func,
			lazy=self.lazy
		))


class Signaller(QtCore.QObject):
	signal = QtCore.Signal(str)

	def __init__(self):
		super().__init__()


class MainThreadOperation(QtWidgets.QWidget):
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
def do_in_ui_thread(func):
	_main_thread_operation(func)