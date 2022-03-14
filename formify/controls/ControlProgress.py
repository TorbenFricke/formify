from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing


class ControlProgress(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QProgressBar()
		self.control.valueChanged.connect(lambda : self.change())

		return self.control

	def get_value(self):
		return self.control.value()

	def set_value(self, value):
		self.control.setValue(value)

	@property
	def maximum(self):
		return self.control.maximum()
	
	@maximum.setter
	def maximum(self, value):
		self.control.setMaximum(value)
	
	@property
	def minimum(self):
		return self.control.minimum()
	
	@minimum.setter
	def minimum(self, value):
		self.control.setMinimum(value)

	@property
	def percentage_visible(self):
		return self.control.isTextVisible()

	@percentage_visible.setter
	def percentage_visible(self, value):
		self.control.setTextVisible(value)

	def spin(self):
		self.maximum = 0
		self.minimum = 0
		self.percentage_visible = False