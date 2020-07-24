from PySide2 import QtWidgets, QtCore
import typing


class ControlBase:
	alignment_flag = QtCore.Qt.AlignTop

	def __init__(self,
	             label:str=None,
	             variable_name:str=None,
	             value:typing.Any=None,
	             parent:QtWidgets.QWidget=None,
	             on_change:typing.Callable=None,
	             **kwargs):
		"""
		Base Class for all controls. On its own, this is just a Label in a BoxLayout.

		:param label: Text for the label.
		:param variable_name: Variable name, if this control is inside a ControlledForm.
		:param kwargs:
		"""
		self.variable_name = variable_name
		self.parent = parent

		# event handling
		self._change_subscriptions = []
		if on_change is not None:
			self.subscribe_change(on_change)

		if label is None:
			if variable_name is None:
				label = self.__class__.__name__
			else:
				label = variable_name

		self._make_label_widget(label)
		self.layout = self._formset()

		# set the new value
		self._value = value
		if not value is None:
			self.value = value


	def _make_label_widget(self, label):
		self.label_widget = QtWidgets.QLabel(text=label, parent=self.parent)
		self.label_widget.setMargin(0)

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		# to be implemented by subclass
		pass

	def _formset(self) -> QtWidgets.QLayout:
		layout = QtWidgets.QVBoxLayout(parent=self.parent)
		layout.setAlignment(self.alignment_flag)
		layout.setMargin(0)
		layout.setSpacing(3)
		layout.addWidget(self.label_widget)

		controls = self._make_control_widget()
		if not controls is None:
			layout.addWidget(controls)

		return layout

	def subscribe_change(self, handler):
		self._change_subscriptions.append(handler)

	def unsubscribe_change(self, handler):
		try:
			del self._change_subscriptions[self._change_subscriptions.index(handler)]
		except:
			return False
		return True

	def _on_change(self, value: typing.Any=None):
		# to be called by subclass, when value changes
		if value is None:
			value = self.value
		for handler in self._change_subscriptions:
			try:
				# Try to provide the handler with the sender and the new value....
				handler(self, value)
			except TypeError:
				# ... if that fails, try just to call it
				handler()

	@property
	def label(self):
		return self.label_widget.text()

	@label.setter
	def label(self, value):
		self.label_widget.setText(value)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value