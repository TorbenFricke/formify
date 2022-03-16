from formify.controls import ControlBase
from PySide6 import QtWidgets, QtGui
import typing


class ControlText(ControlBase):
	_line_edit_validator = None

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		def on_change():
			# catch errors on the on change function, as a ControlFloat might fail while writing
			# something like "2e-3"
			try:
				self.change()
			except ValueError:
				pass

		self.control = QtWidgets.QLineEdit(parent=self)
		self.control.textChanged.connect(on_change)

		# optionally set a validator
		if not self._line_edit_validator is None:
			self.control.setValidator(self._line_edit_validator)

		return self.control

	def get_value(self):
		return self.control.text()

	def set_value(self, value):
		self.control.setText(value)
