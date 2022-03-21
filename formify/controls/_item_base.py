import typing
from formify.controls._events import EventDispatcher
from formify.controls._base import ControlBase


class NamesChangeDetector:
	def __init__(self):
		self._prev_names = None

	def changed(self, new_names):
		try:
			if self._prev_names is None:
				return True

			if len(self._prev_names) != len(new_names):
				return True

			# check if item changed
			for i, new_name in enumerate(new_names):
				current_name = self._prev_names[i]
				if current_name != new_name:
					return True
			return False

		finally:
			self._prev_names = new_names


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

		self._display_names_change_detector = NamesChangeDetector()

		# display name callback is a dict?
		if isinstance(display_name_callback, dict):
			# put it into known filenames...
			self.known_display_names = display_name_callback
			# ... and set display_name_callback to default value
			display_name_callback = str
		else:
			self.known_display_names = {}

		self.display_name_callback = display_name_callback
		self._items = []

		if items is not None:
			if isinstance(items, dict):
				self.known_display_names.update(items)
				self.items = list(items.keys())
			else:
				self.items = items

	def display_names(self, _items):
		if _items is None:
			return []
		return list(map(self.display_name, _items))

	def display_name(self, item):
		# display name is known
		try:
			return self.known_display_names[item]
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

		if self._display_names_change_detector.changed(display_names):
			self.set_display_names(display_names)

		## set the correct index
		# index was -1 but and item was added
		if index == -1 and len(items) > 0:
			self.index = 0

		# no items remaining
		elif len(items) == 0:
			if index != -1:
				self.index = -1

		# index is fine and does not need to be adjusted
		elif len(items) > index:
			self.index = index

		# not enough items - reduce index by
		elif len(items) <= index:
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
			self.known_display_names[value] = label
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
		index = self.index
		if index >= len(self._items):
			index = len(self._items) - 1
		return self._items[index]

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


class SelectBase(ItemBase):

	def set_items(self, items):
		value_before = self.selected_item

		# change the actual items and display names
		with \
				self.index_change.suspend_updates(), \
				self.items_change.suspend_updates(), \
				self.selected_item_change.suspend_updates():
			super().set_items(items)

		# set previous value - if value before not in list -> index remains unchanged
		if not self.set_index_by_item(value_before):
			# index unchanged, but selected item changed
			self.selected_item_change(self.selected_item)

		# finally trigger items change event
		self.index_change(self.index)
		self.items_change(self._items)

	def get_value(self):
		return self.get_selected_item()

	def set_value(self, value):
		if value not in self.items:
			self.items += [value]

		self.set_index_by_item(value)


class SelectControlBase(ControlBase, SelectBase):
	def __init__(
			self,
			label: str = None,
			items: typing.Union[list, dict] = None,
			value=None,
			display_name_callback=str,
			on_change=None,
			*args,
			**kwargs
	):
		ControlBase.__init__(
			self,
			label,
			*args,
			creat_change_event=False,
			**kwargs
		)

		SelectBase.__init__(self, items, display_name_callback)
		self.change = self.selected_item_change

		if on_change is not None:
			self.change.subscribe(on_change)

		if value is not None:
			self.value = value

	def get_value(self):
		return self.get_selected_item()

	def set_value(self, value):
		if value not in self.items:
			self.items += [value]

		self.set_index_by_item(value)


class ListBase(ItemBase):

	def set_items(self, items):
		value_before = self.selected_item

		# change the actual items and display names
		with \
				self.index_change.suspend_updates(), \
				self.items_change.suspend_updates(), \
				self.selected_item_change.suspend_updates():
			super().set_items(items)

		# set previous value - if value before not in list -> index remains unchanged
		if not self.set_index_by_item(value_before):
			# index unchanged, but selected item changed
			self.selected_item_change(self.selected_item)

		# finally trigger items change event
		self.index_change(self.index)
		self.items_change(self._items)

	def get_value(self):
		return self.items

	def set_value(self, value):
		self.items = value


class ListControlBase(ControlBase, ListBase):
	def __init__(
			self,
			label: str = None,
			value: typing.Union[list, dict] = None,
			display_name_callback=str,
			on_change: callable = None,
			add_click: typing.Callable = None,
			remove_click: typing.Callable = None,
			*args,
			**kwargs
	):
		if "value" in kwargs:
			raise TypeError("Use 'value' instead of 'items' if you are using a ControlList*")

		# events
		if add_click is None:
			add_click = lambda : print("No 'add_click' handler was passed to the ControlList. Doing nothing.")
		self.add_click = add_click
		self.remove_click = self.remove_current_item
		if remove_click is not None:
			self.remove_click = remove_click

		ControlBase.__init__(
			self,
			label,
			*args,
			creat_change_event=False,
			**kwargs
		)

		ListBase.__init__(self, value, display_name_callback)
		self.change = self.items_change

		if on_change is not None:
			self.change.subscribe(on_change)

	def get_value(self):
		return self.items

	def set_value(self, value):
		self.items = value

	def remove_current_item(self):
		if len(self._items) == 0:
			return
		del self._items[self.index]
		self.items = self._items