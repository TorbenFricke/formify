from formify.controls._item_base import SelectControlBase, ListControlBase
from PySide6 import QtWidgets
import typing


class ControlSelect(SelectControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change(self.control.currentIndex())
		)

		return self.control

	def get_index(self) -> int:
		return self.control.currentIndex()

	def set_index(self, index: int):
		self.control.setCurrentIndex(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		self.control.clear()
		self.control.addItems(display_names)


class ControlListDropdown(ListControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change(self.control.currentIndex())
		)

		return self.control

	def get_index(self) -> int:
		return self.control.currentIndex()

	def set_index(self, index: int):
		self.control.setCurrentIndex(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		self.control.clear()
		self.control.addItems(display_names)

