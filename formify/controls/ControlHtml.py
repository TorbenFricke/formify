from formify.controls import ControlBase
from PySide2 import QtWidgets, QtCore
import typing

class ControlHtml(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		from PySide2 import QtWebEngineWidgets
		self.control = QtWebEngineWidgets.QWebEngineView()
		self.control.urlChanged.connect(lambda : self.change())

		return self.control

	@property
	def value(self):
		return self.control.page()

	@value.setter
	def value(self, value):
		self.control.setHtml(value)
