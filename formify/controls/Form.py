from formify.controls._mixins import ValueMixin
from PySide2 import QtWidgets
import typing

def _walk(widget) -> typing.List[ValueMixin]:
	controls = []
	for child in widget.children():
		if isinstance(child, ValueMixin):
			# print(f"{child} is a control with variable {child.variable_name}")
			controls.append(child)
		elif isinstance(child,QtWidgets.QWidget):
			#print(f"{child} is not a control")
			controls += _walk(child)
	return controls

__FLATTEN__ = "__flatten__"

class Form(QtWidgets.QWidget, ValueMixin):
	def __init__(self,
	             layout:QtWidgets.QLayout,
	             variable_name: str = None,
	             value: typing.Any = None,
	             on_change: typing.Callable = None,
	             parent:QtWidgets.QWidget=None,):
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

		ValueMixin.__init__(self, variable_name=variable_name, value=value, on_change=on_change)
		QtWidgets.QWidget.__init__(self, parent=parent)

		self.setLayout(layout)
		# Forms should not add any margin
		layout.setMargin(0)
		self.controls = self.get_controls()
		self._subscribe_to_controls()


	def get_controls(self):
		controls = _walk(self)
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


	@property
	def value(self):
		out = {}
		for control in self.controls:
			value = control.value
			variable = control.variable_name
			if variable == __FLATTEN__ and isinstance(value, dict):
				out.update(value)
			else:
				out[variable] = value
		return out


	@value.setter
	def value(self, value):
		relevant_values = {}

		# set child values
		with self.change.suspend_updates():
			for control in self.controls:
				variable = control.variable_name

				# keep track of relevant values
				if variable in value:
					relevant_values[variable] = value[variable]

				# update flattened forms
				if variable == __FLATTEN__ and isinstance(control, Form):
					# set child values
					control.value = value
					# remember, which values were set
					child_variables = [c.variable_name for c in control.controls]
					relevant_values.update({
						key: val for key, val in value.items() if key in child_variables
					})
				else:
					# set all other controls
					if variable in relevant_values:
						control.value = relevant_values[variable]

		# trigger the event manually
		self.change(relevant_values)
