from PySide6 import QtWidgets, QtCore
import typing
from formify import app
from formify.controls._value_base import ValueBase


class ControlBase(QtWidgets.QWidget, ValueBase):
	alignment_flag = QtCore.Qt.AlignTop
	_layout_class = QtWidgets.QVBoxLayout

	def __init__(
			self,
			label: str = None,
			variable_name: str = None,
			value: typing.Any = None,
			parent: QtWidgets.QWidget = None,
			on_change: typing.Callable = None,
			creat_change_event: bool = True,
			**kwargs,
	):
		"""
		Base Class for most controls. On its own, this is just a Label in a BoxLayout.

		:param label: Text for the label.
		:param variable_name: Variable name, if this control is inside a ControlledForm.
		"""
		QtWidgets.QWidget.__init__(self, parent=parent)

		if label is None:
			if variable_name is None:
				label = ""
			else:
				label = app.translator(variable_name)

		self._make_label_widget(label)
		self.layout = self._formset()
		self.setLayout(self.layout)
		self.label = label

		ValueBase.__init__(
			self,
			variable_name=variable_name,
			on_change=on_change,
			value=value,
			creat_change_event=creat_change_event
		)

		set_props(self, kwargs)

	def _make_label_widget(self, label):
		self.label_widget = QtWidgets.QLabel(text=label, parent=self)
		self.label_widget.setMargin(0)
		self.label_widget.setWordWrap(True)

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		# to be implemented by subclass
		raise NotImplementedError

	def _make_control_widgets(self) -> typing.List[QtWidgets.QWidget]:
		# to be implemented by subclass if multiple widgets shall be created
		raise NotImplementedError

	def make_layout(self):
		layout = self._layout_class()
		layout.setAlignment(self.alignment_flag)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(3)
		return layout

	def _formset(self) -> QtWidgets.QLayout:
		layout = self.make_layout()
		layout.addWidget(self.label_widget)

		try:
			control = self._make_control_widget()
			layout.addWidget(control)
		except NotImplementedError:
			try:
				for control in self._make_control_widgets():
					layout.addWidget(control)
			except NotImplementedError:
				pass

		return layout

	@property
	def label(self):
		return self.label_widget.text()

	@label.setter
	def label(self, value):
		self.label_widget.setVisible(value != "")
		self.label_widget.setText(value)


def set_props(self, kwargs):
	for _attr, _item in kwargs.items():
		words = _attr.split("_")
		func_name = "set" + "".join([
			word.capitalize() for word in words
		])

		try:
			func = getattr(self, func_name)
		except AttributeError as e:
			raise AttributeError(f"Cannot set '{_attr}' of '{self.__class__.__name__}' object; {e.args[0]}")
		func(_item)