from formify.controls._mixins import ValueMixin
from formify import app
from PySide6 import QtWidgets
import typing


class ControlCheckbox(ValueMixin, QtWidgets.QCheckBox):
	def __init__(self,
	             label: str = None,
	             variable_name: str = None,
	             value: typing.Any = None,
	             parent: QtWidgets.QWidget = None,
	             on_change: typing.Callable = None):

		if label is None:
			if variable_name is None:
				label = self.__class__.__name__
			else:
				label = app.translator(variable_name)

		QtWidgets.QCheckBox.__init__(self, parent=parent, text=label)

		ValueMixin.__init__(self, variable_name=variable_name, on_change=on_change, value=value)

		# set the on change handler
		self.stateChanged.connect(
			lambda: self.change()
		)

	@property
	def value(self):
		return self.isChecked()

	@value.setter
	def value(self, value):
		self.setChecked(value)



