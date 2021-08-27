import typing
from formify.controls._events import EventDispatcher


class ValueBase:
	def __init__(
			self,
			variable_name: str = None,
			value: typing.Any = None,
			on_change: typing.Callable = None,
			creat_change_event: bool = True,
	):

		self.variable_name = variable_name

		# event handling
		self.change = None
		if creat_change_event:
			self.change = EventDispatcher(self)

		if on_change is not None:
			self.change.subscribe(on_change)

		# set the new value
		if value is not None:
			self.value = value

		# set tooltip
		try:
			if variable_name is not None:
				self.setToolTip(f"Variable: {variable_name}")
		except:
			pass

	def get_value(self):
		raise NotImplementedError

	def set_value(self, value):
		raise NotImplementedError

	def get_all_values(self):
		return self.get_value()

	def set_all_values(self, value):
		self.set_value(value)

	@property
	def value(self):
		return self.get_value()

	@value.setter
	def value(self, value):
		self.set_value(value)

	@property
	def all_values(self):
		return self.get_all_values()

	@all_values.setter
	def all_values(self, value):
		self.set_all_values(value)


