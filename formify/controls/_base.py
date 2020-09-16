from PySide2 import QtWidgets, QtCore
import typing

from formify.controls._mixins import ValueMixin

class ControlBase(QtWidgets.QWidget, ValueMixin):
	alignment_flag = QtCore.Qt.AlignTop
	_layout_class = QtWidgets.QVBoxLayout

	def __init__(self,
	             label:str=None,
	             variable_name:str=None,
	             value:typing.Any=None,
	             parent:QtWidgets.QWidget=None,
	             on_change:typing.Callable=None):
		"""
		Base Class for all controls. On its own, this is just a Label in a BoxLayout.

		:param label: Text for the label.
		:param variable_name: Variable name, if this control is inside a ControlledForm.
		"""
		QtWidgets.QWidget.__init__(self, parent=parent)

		if label is None:
			if variable_name is None:
				label = ""
			else:
				label = variable_name

		self._make_label_widget(label)
		self.layout = self._formset()
		self.setLayout(self.layout)
		self.label = label

		ValueMixin.__init__(self, variable_name=variable_name, on_change=on_change, value=value)


	def _make_label_widget(self, label):
		self.label_widget = QtWidgets.QLabel(text=label, parent=self)
		self.label_widget.setMargin(0)

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		# to be implemented by subclass
		pass

	def _make_control_widgets(self) -> typing.List[QtWidgets.QWidget]:
		# to be implemented by subclass if multiple widgets shall be created
		return []

	def make_layout(self):
		layout = self._layout_class()
		layout.setAlignment(self.alignment_flag)
		layout.setMargin(0)
		layout.setSpacing(3)
		return layout

	def _formset(self) -> QtWidgets.QLayout:
		layout = self.make_layout()
		layout.addWidget(self.label_widget)

		control = self._make_control_widget()
		if not control is None:
			layout.addWidget(control)
		for control in self._make_control_widgets():
			layout.addWidget(control)

		return layout

	@property
	def label(self):
		return self.label_widget.text()

	@label.setter
	def label(self, value):
		self.label_widget.setVisible(value != "")
		self.label_widget.setText(value)
