import typing, copy
from formify.controls._events import EventDispatcher
from collections import Iterable
from PySide2 import QtWidgets

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

		# set tooltip
		try:
			if variable_name is not None:
				self.setToolTip(f"Variable: {variable_name}")
		except:
			pass

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



class ItemMixin:
	def __init__(self, items):
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
		index = self.index

		display_names = [
			name for _, name in self._items
		]
		self.set_display_names(display_names)

		## set the correct index
		# index was -1 but and item was added
		if index == -1 and len(self._items) > 0:
			self.index = 0

		# no items remaining
		elif len(self._items) == 0:
			if index != -1:
				self.index = -1

		# index is fine and does not need to be adjusted
		elif len(self._items) > index:
			# do noting
			pass

		# not enough items - reduce index by
		elif len(self._items) > 0:
			self.index = len(self._items) - 1

		# trigger event
		self.items_change(self._items)

	@property
	def selected_item(self):
		if len(self._items) == 0:
			return None, None
		return self._items[self.index]

	@selected_item.setter
	def selected_item(self, value):
		if len(self._items) == 0:
			self._items = [value]
			self.items = self._items
			self.index = 0
		else:
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
