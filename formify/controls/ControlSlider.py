from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing


class SetPropContext:
	def __init__(self, slider: 'ControlSlider'):
		self.slider = slider
		self.prev_value = None

	def __enter__(self):
		self.prev_value = self.slider.value

	def __exit__(self, exc_type, exc_val, exc_tb):
		with self.slider.change.suspend_updates():
			self.slider.value = self.prev_value


class ControlSlider(ControlBase):
	def __init__(
			self,
			*args,
			minimum: float = 0,
			maximum: float = 100,
			ticks: int = 20,
			**kwargs,
	):
		self._minimum = minimum
		self._maximum = maximum
		self._ticks = ticks
		ControlBase.__init__(self, *args, **kwargs)

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QSlider(QtCore.Qt.Horizontal)

		self.control.setMinimum(0)
		self.control.setMaximum(self._ticks)
		self.control.setTickInterval(1)
		self.control.setPageStep(1)

		self.control.valueChanged.connect(lambda: self.change())

		return self.control

	def set_props(self):
		return SetPropContext(self)

	@property
	def minimum(self):
		return self._minimum

	@minimum.setter
	def minimum(self, value):
		with self.set_props():
			self._minimum = value

	@property
	def ticks(self) -> int:
		return self._ticks

	@ticks.setter
	def ticks(self, value: int):
		with self.set_props():
			self._ticks = value
			self.control.setMaximum(value)

	@property
	def maximum(self):
		return self.maximum

	@maximum.setter
	def maximum(self, value):
		with self.set_props():
			self._maximum = value

	def get_value(self):
		int_value = self.control.value()
		return self._minimum + (self._maximum - self._minimum) * int_value / self._ticks

	def set_value(self, value):
		int_value = (value - self._minimum) / (self._maximum - self.minimum) * self._ticks
		int_value = int(round(int_value))
		self.control.setValue(int_value)
