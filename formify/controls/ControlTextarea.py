from formify.controls import ControlBase
from PySide2 import QtWidgets, QtCore
import typing

class ControlTextarea(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QTextEdit()
		self.control.textChanged.connect(lambda : self.change())

		return self.control

	@property
	def value(self):
		return self.control.toPlainText()

	@value.setter
	def value(self, value):
		self.control.setPlainText(value)

	@property
	def read_only(self):
		return self.control.isReadOnly()

	@read_only.setter
	def read_only(self, value):
		return self.control.setReadOnly(value)