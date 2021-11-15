from formify.controls import ControlBase
from PySide6 import QtWidgets
from formify.layout import ensure_widget, Row
from formify.controls import ControlButton
from formify.tools import open_dialog
from formify import app
import typing


class ControlFile(ControlBase):

	def show_dialog(self):
		fn = open_dialog(self.value)
		if fn:
			self.value = fn

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

		self.button = ControlButton(app.translator("Open..."), on_click=self.show_dialog)

		return ensure_widget(
			Row(self.control, self.button)
		)

	def get_value(self):
		return self.control.text()

	def set_value(self, value):
		self.control.setText(value)
