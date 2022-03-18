from formify.controls._value_base import ValueBase
from formify.layout import ensure_layout
from formify.controls._base import set_props
from PySide6 import QtWidgets
import typing


def walk(widget) -> typing.List[ValueBase]:
	controls = []
	for child in widget.children():
		if isinstance(child, ValueBase):
			# print(f"{child} is a control with variable {child.variable_name}")
			controls.append(child)
		elif isinstance(child, QtWidgets.QWidget):
			# print(f"{child} is not a control")
			controls += walk(child)
	return controls


def extract_values_dict(controls, all_values=False):
	out = {}
	for control in controls:
		if all_values:
			value = control.all_values
		else:
			value = control.value
		variable = control.variable_name
		if variable == __FLATTEN__ and isinstance(value, dict):
			out.update(value)
		else:
			out[variable] = value
	return out


def set_values(controls, data, relevant_values, all_values=False):
	for control in controls:
		variable = control.variable_name

		# keep track of relevant values
		if variable in data:
			relevant_values[variable] = data[variable]

		# update flattened forms
		if variable == __FLATTEN__ and isinstance(control, Form):
			# set child values
			if all_values:
				control.all_value = data
			else:
				control.value = data
			# remember, which values were set
			child_variables = [c.variable_name for c in control.controls]
			relevant_values.update({
				key: val for key, val in data.items() if key in child_variables
			})
		else:
			# set all other controls
			if variable in relevant_values:
				if all_values:
					control.all_value = relevant_values[variable]
				else:
					control.value = relevant_values[variable]


__FLATTEN__ = "__flatten__"


class Form(QtWidgets.QWidget, ValueBase):
	def __init__(
			self,
			layout: typing.Union[QtWidgets.QLayout, QtWidgets.QWidget],
			variable_name: str = None,
			value: typing.Any = None,
			on_change: typing.Callable = None,
			parent: QtWidgets.QWidget = None,
			**kwargs,
	):
		"""
		Acts as a master control for all controls inside the "layout" that include a variable name.

		:param layout: QLayout that includes the controls for the Form
		:param variable_name: Variable name of the form itself. There is one special case:
		If the variable name "__flatten__" is used inside a child form, its values are included directly
		in this forms values.
		Normal behavior: "{"child_form_variable_name": {"control1": 1, "control_b": 2}}"
		__flatten__ behavior: "{"control1": 1, "control_b": 2}"
		:param value: Dict of all the child control values
		:param on_change: One change handler. Internally calls subscribe_change(on_change).
		:param parent:
		"""

		QtWidgets.QWidget.__init__(self, parent=parent)
		ValueBase.__init__(self, variable_name=variable_name, value=value, on_change=on_change)

		layout = ensure_layout(layout)
		self.setLayout(layout)
		# Forms should not add any margin by default
		layout.setContentsMargins(0, 0, 0, 0)
		self.controls = self.get_controls()
		self._subscribe_to_controls()

		set_props(self, kwargs)

	def get_controls(self):
		controls = walk(self)
		controls = [control for control in controls if control.variable_name is not None]
		return controls

	def _on_child_change(self, sender, value):
		# this method is passed as a handler to all child controls
		if sender.variable_name == __FLATTEN__:
			self.change(value)
		else:
			self.change({
				sender.variable_name: value
			})

	def _subscribe_to_controls(self):
		for control in self.controls:
			control.change.subscribe(self._on_child_change)

	def __getitem__(self, key) -> ValueBase:
		for control in self.controls:
			variable = control.variable_name

			if variable == key:
				return control

			# update flattened forms
			if variable == __FLATTEN__ and isinstance(control, Form):
				flattened_control = control[key]
				if flattened_control is not None:
					return flattened_control

	def get_value(self):
		return extract_values_dict(self.controls)

	def set_value(self, value):
		self.set_values(value)

	def set_values(self, data, all_values=False):
		relevant_values = {}

		# set child values
		with self.change.suspend_updates():
			for control in self.controls:
				variable = control.variable_name

				# keep track of relevant values
				if variable in data:
					relevant_values[variable] = data[variable]

				# update flattened forms
				if variable == __FLATTEN__ and isinstance(control, Form):
					# set child values
					if all_values:
						control.all_values = data
					else:
						control.value = data
					# remember, which values were set
					child_variables = [c.variable_name for c in control.controls]
					relevant_values.update({
						key: val for key, val in data.items() if key in child_variables
					})
				else:
					# set all other controls
					if variable in relevant_values:
						if all_values:
							control.all_values = relevant_values[variable]
						else:
							control.value = relevant_values[variable]

		# trigger the event manually
		self.change(relevant_values)

	def get_all_values(self):
		return extract_values_dict(self.controls, all_values=True)

	def set_all_values(self, value):
		self.set_values(value, all_values=True)

