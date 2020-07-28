from formify.controls import ControlCombo
from PySide2 import QtWidgets
import typing


class ComboComboList(ControlCombo):

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QListWidget(parent=self)

		# add items
		for key, display_name in self._items:
			self.control.addItem(display_name)
		if len(self._items) > 0:
			self.control.setCurrentRow(0)

		# set the on change handler
		self.control.itemSelectionChanged.connect(
			lambda: self._on_change()
		)

		return self.control

	@property
	def value(self):
		return self._items[self.control.currentRow()][0]

	@value.setter
	def value(self, value):
		for i, item in enumerate(self._items):
			if item[1] == value:
				self.control.setCurrentRow(i)
				return
