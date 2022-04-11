from formify.controls._base import set_props
from PySide6 import QtWidgets, QtCore
import warnings


class Signaller(QtCore.QObject):
	signal = QtCore.Signal(str)

	def __init__(self):
		super().__init__()


class ControlPyvista(QtWidgets.QWidget):
	def __init__(
			self,
			parent: QtWidgets.QWidget = None,
			**kwargs,
	):
		QtWidgets.QWidget.__init__(self, parent=parent)

		# importing matplotlib takes a while, so we only do it if required
		import os
		os.environ["QT_API"] = "pyside6"

		try:
			from pyvistaqt import BackgroundPlotter
			from pyvistaqt import QtInteractor
		except IndexError as e:
			raise IndexError("Please run 'pip install pyvista' and 'pip install pyvistaqt'. " + e.args[0])

		self.plotter = QtInteractor(self)

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.plotter)
		layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(layout)

		set_props(self, kwargs)
