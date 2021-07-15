import typing
from formify.controls._events import EventDispatcher


class ItemBase:
	def __init__(
			self,
			items: typing.Union[list, dict, None] = None,
			display_name_callback: typing.Union[dict, callable] = str
	):
		self.items_change = EventDispatcher(self)
		self.index_change = EventDispatcher(self)
		self.selected_item_change = EventDispatcher(self)

		self.index_change.subscribe(
			lambda: self.selected_item_change(self.get_selected_item())
		)

		# display name callback is a dict?
		if isinstance(display_name_callback, dict):
			# put it into known filenames...
			self._known_display_names = display_name_callback
			# ... and set display_name_callback to default value
			display_name_callback = str
		else:
			self._known_display_names = {}

		self.display_name_callback = display_name_callback
		self._items = []

		if items is not None:
			if isinstance(items, dict):
				self._known_display_names.update({
					value: key for key, value in items.items()
				})
				items = list(items.values())
			self.items = items

	def display_names(self, _items):
		if _items is None:
			return []
		return list(map(self.display_name, _items))

	def display_name(self, item):
		# display name is known
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

	@property
	def items(self):
		return self._items if self._items is not None else []

	@items.setter
	def items(self, value):
		self.set_items(value)

	def set_items(self, items):
		if items is None:
			items = []

		# get list of display names based on new items
		display_names = self.display_names(items)

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
			self.index = index

		# not enough items - reduce index by
		elif len(self._items) > 0:
			self.index = len(self._items) - 1

		# trigger event
		self.items_change(self._items)

	@property
	def selected_item(self):
		return self.get_selected_item()

	@selected_item.setter
	def selected_item(self, value):
		self.set_selected_item(value)

	@property
	def index(self) -> int:
		return self.get_index()

	@index.setter
	def index(self, value: int):
		self.set_index(value)

	def append(self, value, label=None):
		if label is not None:
			self._known_display_names[value] = label
		self.items = self.items + [value]

	def set_display_names(self, display_names):
		raise NotImplemented

	def get_index(self) -> int:
		raise NotImplemented

	def set_index(self, index: int):
		raise NotImplemented

	def get_selected_item(self):
		if len(self._items) == 0:
			return None
		return self._items[self.index]

	def set_selected_item(self, item):
		if len(self._items) == 0:
			self._items = [item]
			self.items = self._items
		else:
			self._items[self.index] = item
			self.items = self._items

		self.selected_item_change(item)

	def set_index_by_item(self, item) -> bool:
		# set current index without causing an on change event
		for i, _item in enumerate(self.items):
			if _item == item:
				self.index = i
				return True

		return False
