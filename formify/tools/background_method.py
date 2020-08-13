import typing
from queue import Queue
from threading import Thread


class Task:
	def __init__(self, target, lazy=False):
		self.target = target
		self.lazy = lazy


class BackgroundMethod(Thread):
	def __init__(self, target:typing.Callable, lazy=False, cleanup:typing.Callable=None):
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
			except Exception as e:
				print(e.__traceback__)


	def __call__(self, *args, **kwargs):
		"""
		Executes the self.target with the provided *args and **kwargs.

		:param args:
		:param kwargs:
		:return:
		"""
		self.queue.put(Task(
			lambda : self.target(*args, **kwargs),
			lazy=self.lazy
		))