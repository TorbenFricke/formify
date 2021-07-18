from formify.controls._item_base import SelectControlBase
from PySide6 import QtWidgets
import typing


# TODO ControlList (list), ControlListDropdown, ControlListSidebar
# TODO ControlSelectSidebar, ControlSelectRadio

class ControlSelectControl(SelectControlBase):
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


class ControlSelectControlList(SelectControlBase):
	def _make_control_widget(self) -> typing.List[QtWidgets.QWidget]:
		self.control = QtWidgets.QListWidget(parent=self)
		# set the on change handler
		self.control.itemSelectionChanged.connect(
			lambda: self.index_change(self.index)
		)

		return self.control

	def get_index(self) -> int:
		return self.control.currentRow()

	def set_index(self, index: int):
		self.control.setCurrentRow(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		with self.index_change.suspend_updates():
			self.control.clear()
			if len(display_names) > 0:
				self.control.addItems(display_names)
