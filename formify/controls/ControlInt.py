from formify.controls import ControlText
from PySide6.QtGui import QIntValidator

def _str2int(s:str) -> int:
	if s == "":
		return 0
	try:
		return int(s)
	except:
		return int(float(s))


class ControlInt(ControlText):
	_line_edit_validator = QIntValidator()

	@property
	def value(self) -> int:
		return _str2int(self.control.text())

	@value.setter
	def value(self, value: int):
		self.control.setText(str(value))
