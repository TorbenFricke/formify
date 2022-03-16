from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing


class ControlHtml(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		from PySide6 import QtWebEngineWidgets
		self.control = QtWebEngineWidgets.QWebEngineView()
		self.control.urlChanged.connect(lambda : self.change())

		return self.control

	def get_value(self):
		return self.control.page()

	def set_value(self, value):
		self.control.setHtml(value)
