from formify.controls import ControlBase
from formify.controls._events import EventDispatcher
from PySide6 import QtWidgets
import typing

from formify.controls._mixins import ItemMixin


class ControlCombo(ControlBase, ItemMixin):
	def __init__(self,
				 label: str = None,
				 items: list = None,
				 value=None,
				 display_name_callback=str,
				 *args,
				 **kwargs):

		self.index_change = EventDispatcher(self)

		ControlBase.__init__(self,
							 label,
							 *args,
							 **kwargs)

		# normalize items array
		ItemMixin.__init__(self, items, display_name_callback)

		if value is not None:
			self.value = value
		elif items is not None and len(items) > 0:
			self.value = items[0]

		self.index_change.subscribe(self._index_change_handler)

	def _index_change_handler(self):
		value_before = self._value
		try:
			value_from_index = self.items[self.index]
		except IndexError:
			return
		if value_from_index != value_before:
			self._value = value_from_index
			self.change(value_from_index)

	@property
	def index(self) -> int:
		return self.control.currentIndex()

	@index.setter
	def index(self, value: int):
		self.control.setCurrentIndex(value)

	def set_display_names(self, display_names):
		# add items
		with self.change.suspend_updates():
			value_before = self.value
			self.control.clear()
			self.control.addItems(display_names)
			self.value = value_before

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change()
		)

		return self.control

	@property
	def value(self):
		try:
			return self.items[self.index]
		except IndexError:
			return None

	@value.setter
	def value(self, value):
		# cause the event now
		if not value in self.items:
			self.items.append(value)

		# set currect index without causing an on change event
		for i, item in enumerate(self.items):
			if item == value:
				self.index = i
