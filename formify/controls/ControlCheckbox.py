from formify.controls import ControlBase
from PySide2 import QtWidgets, QtCore
import typing


class ControlCheckbox(ControlBase):
	def _make_label_widget(self, label):
		# in this case this actually creates the one and only widget - a QCheckBox
		self.label_widget = self.control = QtWidgets.QCheckBox(parent=self, text=label)

		# set the on change handler
		self.control.stateChanged.connect(
			lambda: self._on_change()
		)

	@property
	def value(self):
		return self.control.isChecked()

	@value.setter
	def value(self, value):
		self.control.setChecked(value)
