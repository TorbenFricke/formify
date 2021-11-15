from formify.controls import ControlText
from PySide6.QtGui import QDoubleValidator, QValidator


def _str2float(s) -> float:
	if s == "":
		return 0
	if type(s) == str:
		return float(s.replace(",", "."))
	return float(s)


class CustomDoubleValidator(QDoubleValidator):
	def validate(self, arg__1, arg__2):
		validation_data = super().validate(arg__1, arg__2)

		if validation_data[0] == QValidator.State.Intermediate:
			try:
				_str2float(arg__1)
				return QValidator.Acceptable, arg__1, arg__2
			except ValueError:
				pass

		return validation_data


class ControlFloat(ControlText):
	_line_edit_validator = CustomDoubleValidator()

	def __init__(self, *args, **kwargs):
		self._factor = kwargs.pop("factor", 1)
		super().__init__(*args, **kwargs)

	def get_value(self):
		return _str2float(self.control.text()) * self._factor

	def set_value(self, value):
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
