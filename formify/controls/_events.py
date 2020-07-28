import typing


class suspend_updates:
	def __init__(self, form):
		self.form = form

	def __enter__(self):
		self.form._suspend_update_events = True
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.form._suspend_update_events = False


class EventDispatcher:
	def __init__(self, parent):
		self.parent = parent
		self.subscriptions = []
		self._suspend_update_events = False

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
		if self._suspend_update_events:
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


	def suspend_updates(self):
		return suspend_updates(self)