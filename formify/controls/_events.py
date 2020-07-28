import typing


class EventDispatcher:
	def __init__(self, parent):
		self.parent = parent
		self.subscriptions = []

	def subscribe(self, handler):
		self.subscriptions.append(handler)

	def unsubscribe(self, handler):
		try:
			del self.subscriptions[self.subscriptions.index(handler)]
		except:
			return False
		return True

	def trigger(self, value: typing.Any = None):
		# to be called by subclass, when value changes
		if len(self.subscriptions) == 0:
			return
		if value is None:
			value = self.parent.value
		for handler in self.subscriptions:
			try:
				# Try to provide the handler with the sender and the new value....
				handler(self.parent, value)
			except TypeError:
				# ... if that fails, try just to call it
				handler()

	def __call__(self, value: typing.Any = None):
		self.trigger(value)