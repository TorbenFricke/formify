import typing


class suspend_updates:
	def __init__(self, event):
		self.event = event

	def __enter__(self):
		self.event._suspend_update_count += 1
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.event._suspend_update_count -= 1


class EventDispatcher:
	def __init__(self, parent):
		self.parent = parent
		self.subscriptions = []
		self._suspend_update_count = 0

	def subscribe(self, handler):
		self.subscriptions.append(handler)

	def unsubscribe(self, handler):
		try:
			del self.subscriptions[self.subscriptions.index(handler)]
		except:
			return False
		return True

	def _trigger(self, value: typing.Any = None):
		# to be called by subclass, when value changes
		if len(self.subscriptions) == 0:
			return
		if self._suspend_update_count > 0:
			return
		if value is None:
			value = self.parent.value
		for handler in self.subscriptions:
			try:
				# Try to provide the handler with the sender and the new value....
				handler(self.parent, value)
				continue
			except TypeError:
				pass
			# ... if that fails, try just to call it
			handler()

	def __call__(self, value: typing.Any = None):
		self._trigger(value)


	def suspend_updates(self):
		return suspend_updates(self)