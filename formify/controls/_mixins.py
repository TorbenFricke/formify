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
	def __init__(self, items, display_name_callback: typing.Union[dict, callable] = str):
		self.items_change = EventDispatcher(self)

		# display nam callback is a dict?
		if isinstance(display_name_callback, dict):
			# put it into known filenames...
			self._known_display_names = display_name_callback
			# ... and set display_name_callback to default value
			display_name_callback = str
		else:
			self._known_display_names = {}

		self.display_name_callback = display_name_callback
		self._items = []
		self.items = items

	def display_names(self, _items):
		if _items is None:
			return []
		return list(map(self.display_name, _items))

	def display_name(self, item):
		# provided a label -> use that
		if isinstance(item, tuple) and isinstance(item[1], str):
			value, name = item
			self._known_display_names[value] = name
			return name

		else:
			# file name is known
			try:
				return self._known_display_names[item]
			except:
				pass
			# use the display name callback
			try:
				return self.display_name_callback(item)
			except:
				pass

		# last resort
		return str(item)

	@staticmethod
	def strip_display_names(items):
		def strip_display_name(item):
			if isinstance(item, tuple) and isinstance(item[1], str):
				return item[0]
			return item

		return list(map(strip_display_name, items))

	@property
	def items(self):
		return self._items if self._items is not None else []

	@items.setter
	def items(self, value):
		if value is None:
			value = []

		# seperate actual items and display names
		display_names = self.display_names(value)
		items = self.strip_display_names(value)

		self._items = items
		index = self.index

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
			return None
		return self._items[self.index]

	@selected_item.setter
	def selected_item(self, value):
		if len(self._items) == 0:
			self._items = [value]
			self.items = self._items
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
