from formify.controls._base import ValueMixin
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



class suspend_updates:
	def __init__(self, form):
		self.form = form

	def __enter__(self):
		self.form._suspend_update_events = True
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.form._suspend_update_events = False


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

		self._suspend_update_events = False

		self.setLayout(layout)
		self.all_controls, self.controls_dict = self.get_controls()
		self._subscribe_to_controls()


	def get_controls(self):
		controls = _walk(self)
		controls_dict = {
			control.variable_name: control for control in controls if control.variable_name is not None
		}
		return controls, controls_dict


	def _on_child_change(self, sender, value):
		# this method is passed as a handler to all child controls
		if self._suspend_update_events:
			return
		if sender.variable_name == __FLATTEN__:
			self._on_change(value)
		else:
			self._on_change({
				sender.variable_name: value
			})

	def _subscribe_to_controls(self):
		for key, control in self.controls_dict.items():
			control.subscribe_change(self._on_child_change)


	@property
	def value(self):
		out = {}
		for variable, control in self.controls_dict.items():
			value = control.value
			if variable == __FLATTEN__ and isinstance(value, dict):
				out.update(value)
			else:
				out[variable] = value
		return out


	@value.setter
	def value(self, value):
		relevant_values = {
			key: val for key, val in value.items() if key in self.controls_dict
		}

		# set child values
		with suspend_updates(self):
			for variable, control in self.controls_dict.items():
				# update flattened forms
				if variable == __FLATTEN__ and isinstance(control, Form):
					# set child values
					control.value = value
					# remember, which values were set
					relevant_values.update({
						key: val for key, val in value.items() if key in control.controls_dict
					})
				else:
					# set all other controls
					if variable in self.controls_dict and variable in relevant_values:
						self.controls_dict[variable].value = relevant_values[variable]

		# trigger the event manually
		self._on_change(relevant_values)
