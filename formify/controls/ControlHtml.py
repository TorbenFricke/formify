from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing


class ControlHtml(ControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		try:
			from PySide6 import QtWebEngineWidgets
		except ImportError as e:
			raise ImportError(
				"The QWebEngineView is currently nor supported by PySide6. " + e.args[0]
			)
		self.control = QtWebEngineWidgets.QWebEngineView()
		self.control.urlChanged.connect(lambda : self.change())

		return self.control

	def get_value(self):
		return self.control.page()

	def set_value(self, value):
		self.control.setHtml(value)
