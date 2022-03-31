from formify.controls._base import set_props
from PySide6 import QtWidgets, QtCore
import warnings


class Signaller(QtCore.QObject):
	signal = QtCore.Signal(str)

	def __init__(self):
		super().__init__()


class ControlMatplotlib(QtWidgets.QWidget):
	def __init__(
			self,
			toolbar_visible=True,
			parent: QtWidgets.QWidget = None,
			**kwargs,
	):
		QtWidgets.QWidget.__init__(self, parent=parent)

		# importing matplotlib takes a while, so we only do it if required
		try:
			from matplotlib.figure import Figure
			from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
			from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
		except IndexError as e:
			raise IndexError("Please run 'pip install matplotlib'. " + e.args[0])

		self._fig = Figure((5.0, 4.0), dpi=100)
		self._fig.patch.set_alpha(0)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.toolbar = NavigationToolbar(self.canvas, self)
		self.toolbar_visible = toolbar_visible

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.canvas)
		layout.addWidget(self.toolbar)
		layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(layout)

		# we use a signal to make sure redrawing is done in the main Thread
		self._repaint_signal = Signaller()
		self._repaint_signal.signal.connect(self._actually_draw)

		set_props(self, kwargs)

	@property
	def fig(self):
		return self._fig

	@property
	def toolbar_visible(self):
		return self.toolbar.isVisible()

	@toolbar_visible.setter
	def toolbar_visible(self, value):
		self.toolbar.setVisible(value)

	def draw(self):
		"""
		Draws the figure, like plt.show()
		:return:
		"""
		try:
			self.canvas.draw()
		except Exception as e:
			warnings.warn("Error while drawing matplotlib figure: \n" + str(e))
		self._repaint_signal.signal.emit("emitting")

	@QtCore.Slot(str)
	def _actually_draw(self, value):
		self.repaint()