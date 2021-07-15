from formify.controls import ControlBase
from formify.controls._events import EventDispatcher
from PySide6 import QtWidgets
import typing

from formify.controls._list_base import ItemBase


class ControlCombo(ControlBase, ItemBase):
	def __init__(
		self,
		label: str = None,
		items: typing.Union[list, dict] = None,
		value=None,
		display_name_callback=str,
		*args,
		**kwargs
	):
		ControlBase.__init__(
			self,
			label,
			*args,
			**kwargs
		)
		ItemBase.__init__(self, items, display_name_callback)

		self.change = self.selected_item_change
		if value is not None:
			self.value = value

		#if value is not None:
		#	self.value = value
		#elif items is not None and len(items) > 0:
		#	self.value = items[0]

	def get_index(self) -> int:
		return self.control.currentIndex()

	def set_index(self, index: int):
		self.control.setCurrentIndex(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		with self.change.suspend_updates():
			self.control.clear()
			self.control.addItems(display_names)

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change(self.control.currentIndex())
		)

		return self.control

	def get_value(self):
		return self.get_selected_item()

	def set_value(self, value):
		if value not in self.items:
			self.items += [value]

		self.set_index_by_item(value)

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
		self.items_change(self._items)

