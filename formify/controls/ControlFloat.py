from formify.controls import ControlText
from PySide2.QtGui import QDoubleValidator

def _str2float(s) -> float:
	if s == "":
		return 0
	if type(s) == str:
		return float(s.replace(",", "."))
	return float(s)


class ControlFloat(ControlText):
	_line_edit_validator = QDoubleValidator()

	def __init__(self, *args, **kwargs):
		self._factor = kwargs.pop("factor", 1)
		super().__init__(*args, **kwargs)


	@property
	def value(self):
		return _str2float(self.control.text()) * self._factor

	@value.setter
	def value(self, value):
		self.control.setText(
			str(_str2float(value) / self._factor)
		)


def control_float_factor(factor):
	def make_control(*args, **kwargs):
		kwargs["factor"] = factor
		return ControlFloat(*args, **kwargs)
	return make_control


ControlFloatNano = control_float_factor(1e-9)
ControlFloatMicro = control_float_factor(1e-6)
ControlFloatMilli = control_float_factor(1e-3)
ControlFloatDeci = control_float_factor(10)
ControlFloatKilo = control_float_factor(1e3)
ControlFloatMega = control_float_factor(1e6)
ControlFloatGiga = control_float_factor(1e9)
ControlFloatTerra = control_float_factor(1e12)