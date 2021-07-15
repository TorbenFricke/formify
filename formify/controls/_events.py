import typing


class suspend_updates:
	def __init__(self, event: 'EventDispatcher'):
		self.event = event

	def __enter__(self):
		self.event.suspend_update_count += 1
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.event.suspend_update_count -= 1


class EventDispatcher:
	def __init__(self, parent):
		self.parent = parent
		self.subscriptions = []
		self.suspend_update_count = 0
		self._perv_value = None

	def subscribe(self, handler):
		self.subscriptions.append(handler)

	def unsubscribe(self, handler):
		try:
			del self.subscriptions[self.subscriptions.index(handler)]
		except:
			return False
		return True

	def _trigger(self, value: typing.Any = None):
		# no subcribtions -> no nothing
		if len(self.subscriptions) == 0:
			return
		# updates are suspended?
		if self.suspend_update_count > 0:
			return

		# get current value if none is provided
		if value is None:
			value = self.parent.value

		# check if anything actually changed
		if value == self._perv_value:
			return
		self._perv_value = value

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