from PySide2 import QtWidgets
import typing
from formify.controls._events import EventDispatcher
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import style

class ControlMatplotlib(QtWidgets.QWidget):
	def __init__(self,
	             toolbar_visible=True,
	             parent: QtWidgets.QWidget = None):

		QtWidgets.QWidget.__init__(self, parent=parent)

		self._fig = Figure((5.0, 4.0), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.toolbar = NavigationToolbar(self.canvas, self)
		self.toolbar_visible = toolbar_visible

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.canvas)
		layout.addWidget(self.toolbar)
		layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(layout)

	@property
	def fig(self) -> Figure:
		return self._fig

	@property
	def toolbar_visible(self):
		return self.toolbar.isVisible()

	@toolbar_visible.setter
	def toolbar_visible(self, value):
		self.toolbar.setVisible(value)
