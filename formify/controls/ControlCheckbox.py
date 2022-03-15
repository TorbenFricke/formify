from formify.controls._value_base import ValueBase
from formify import app
from PySide6 import QtWidgets
import typing
from formify.controls._base import set_props


class ControlCheckbox(ValueBase, QtWidgets.QCheckBox):
	def __init__(
			self,
			label: str = None,
			variable_name: str = None,
			value: typing.Any = None,
			parent: QtWidgets.QWidget = None,
			on_change: typing.Callable = None,
			**kwargs
	):

		if label is None:
			if variable_name is None:
				label = self.__class__.__name__
			else:
				label = app.translator(variable_name)

		QtWidgets.QCheckBox.__init__(self, parent=parent, text=label)

		ValueBase.__init__(self, variable_name=variable_name, on_change=on_change, value=value)

		# set the on change handler
		self.stateChanged.connect(
			lambda: self.change()
		)

		set_props(self, kwargs)

	def get_value(self):
		return self.isChecked()

	def set_value(self, value):
		self.setChecked(value)



