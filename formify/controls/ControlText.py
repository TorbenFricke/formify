from formify.controls import ControlBase
from PySide2 import QtWidgets
import typing


class ControlText(ControlBase):
	_line_edit_validator = None

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		def on_change():
			# catch errors on the on change function, as a ControlFloat might fail while writing
			# someting like "2e-3"
			try:
				self._on_change()
			except ValueError:
				pass

		self.control = QtWidgets.QLineEdit(parent=self)
		self.control.textChanged.connect(on_change)

		# optionally set a validator
		if not self._line_edit_validator is None:
			self.control.setValidator(self._line_edit_validator)

		return self.control

	@property
	def value(self):
		return self.control.text()

	@value.setter
	def value(self, value):
		self.control.setText(value)
