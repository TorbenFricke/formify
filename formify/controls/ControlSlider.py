from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing

class ControlSlider(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.control.valueChanged.connect(lambda : self.change())

		return self.control

	@property
	def value(self):
		return self.control.value()

	@value.setter
	def value(self, value):
		self.control.setValue(value)
