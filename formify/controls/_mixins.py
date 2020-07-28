import typing
from formify.controls._events import EventDispatcher

class ValueMixin:
	def __init__(self,
	             variable_name: str = None,
	             value: typing.Any = None,
	             on_change: typing.Callable = None):

		self.variable_name = variable_name

		# event handling
		self.change = EventDispatcher(self)
		if on_change is not None:
			self.change.subscribe(on_change)

		# set the new value
		self._value = value
		if not value is None:
			self.value = value

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value



class ItemMixin:
	def __init__(self, items):
		self._items = []
		self.items = items
		self.index = 0

	@staticmethod
	def key_value(_items):
		if _items is None:
			return []
		for item in _items:
			if type(item) == str:
				yield item, item
			else:
				yield item[0], item[1]

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, value):
		self._items = list(self.key_value(value))
		index = self.index

		# set the items in actual widget
		self.set_items(self._items)

		# set the correct index
		if len(self._items) > index:
			self.index = index
		elif len(self._items) > 0:
			self.index = len(self._items) - 1

	@property
	def index(self) -> int:
		raise NotImplemented

	@index.setter
	def index(self, value: int):
		raise NotImplemented

	def set_items(self, items):
		raise NotImplemented
