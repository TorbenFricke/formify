from formify import app
from formify.controls._value_base import ValueBase
from formify.controls._item_base import SelectControlBase
from formify.layout.segments import Segment
from formify.layout.layouts import Col
from formify.controls._base import set_props
from PySide6 import QtWidgets
import typing


class ControlRadio(ValueBase, QtWidgets.QRadioButton):
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

		QtWidgets.QRadioButton.__init__(self, parent=parent, text=label)

		ValueBase.__init__(self, variable_name=variable_name, on_change=on_change, value=value)

		set_props(self, kwargs)

		# set the on change handler
		self.toggled.connect(
			lambda: self.change()
		)

	def get_value(self):
		return self.isChecked()

	def set_value(self, value):
		self.setChecked(value)


class ControlSelectRadio(SelectControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self._radios = []

		self.radio_layout = Col()
		self.segment = Segment(self.radio_layout)

		return self.segment

	def _make_radio(self, txt):
		radio = QtWidgets.QRadioButton(txt, self.segment)
		self._radios.append(radio)
		self.radio_layout.addWidget(radio)
		radio.toggled.connect(
			lambda: self.index_change(self.index)
		)
		return radio

	def ensure_number_radios(self, n):
		# correct number of _buttons
		if n == len(self._radios):
			return
		# remove _buttons
		while n < len(self._radios):
			radio = self.radio_layout.takeAt(n)
			self._radios.pop(n)
			radio.widget().deleteLater()
		# add _buttons
		while n > len(self._radios):
			self._make_radio("")

	def get_index(self) -> int:
		for i, radio in enumerate(self._radios):
			if radio.isChecked():
				return i
		return -1

	def set_index(self, index: int):
		for i, radio in enumerate(self._radios):
			radio.setChecked(i == index)

		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		self.ensure_number_radios(len(display_names))
		for i, name in enumerate(display_names):
			self._radios[i].setText(name)
