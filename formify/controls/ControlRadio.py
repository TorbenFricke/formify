from formify import app
from formify.controls._value_base import ValueBase
from PySide6 import QtWidgets
import typing


class ControlRadio(ValueBase, QtWidgets.QRadioButton):
	def __init__(
			self,
			label: str = None,
			variable_name: str = None,
			value: typing.Any = None,
			parent: QtWidgets.QWidget = None,
			on_change: typing.Callable = None
	):
		if label is None:
			if variable_name is None:
				label = self.__class__.__name__
			else:
				label = app.translator(variable_name)

		QtWidgets.QRadioButton.__init__(self, parent=parent, text=label)

		ValueBase.__init__(self, variable_name=variable_name, on_change=on_change, value=value)

		# set the on change handler
		self.toggled.connect(
			lambda: self.change()
		)

	def get_value(self):
		return self.isChecked()

	def set_value(self, value):
		self.setChecked(value)



