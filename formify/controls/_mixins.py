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

	@property
	def all_values(self):
		return self.value

	@all_values.setter
	def all_values(self, value):
		self.value = value



class _ListChangeDetector:
	def __init__(self, initial=None):
		self.prev = initial

	def __call__(self, new):
		if self.prev is None:
			self.prev = new
			return True

		if len(new) != len(self.prev):
			self.prev = new
			return True

		for new_item, prev_item in zip(new, self.prev):
			if new_item != prev_item:
				return True

		self.prev = new
		return False


class ItemMixin:
	def __init__(self, items):
		self.display_names_change_detector = _ListChangeDetector()
		self.items_change = EventDispatcher(self)
		self._items = []
		self.items = items

	@staticmethod
	def key_value(_items):
		if _items is None:
			return []
		for item in _items:
			yield ItemMixin.key_value_single(item)

	@staticmethod
	def key_value_single(item):
		if type(item) == str:
			return item, item
		else:
			return item[0], item[1]

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, value):
		self._items = list(self.key_value(value))
		self.items_change(self._items)
		index = self.index

		display_names = [
			name for _, name in self._items
		]
		if not self.display_names_change_detector(display_names):
			return

		# set the items in actual widget
		self.set_display_names(display_names)

		# set the correct index
		if index == -1 and len(self._items) > 0:
			index = 0
		if len(self._items) == 0:
			index = -1
		if len(self._items) > index:
			self.index = index
		elif len(self._items) > 0:
			self.index = len(self._items) - 1

	@property
	def selected_item(self):
		if len(self._items) == 0:
			return None, None
		return self._items[self.index]

	@selected_item.setter
	def selected_item(self, value):
		self._items[self.index] = value
		self.items = self._items


	@property
	def index(self) -> int:
		raise NotImplemented

	@index.setter
	def index(self, value: int):
		raise NotImplemented

	def set_display_names(self, display_names):
		raise NotImplemented
