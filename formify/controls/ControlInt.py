from formify.controls import ControlText
from PySide2.QtGui import QIntValidator


class ControlInt(ControlText):
	_line_edit_validator = QIntValidator()

	@property
	def value(self) -> int:
		return int(self.control.text())

	@value.setter
	def value(self, value: int):
		self.control.setText(str(value))
