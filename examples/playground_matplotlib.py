import sys
from PySide2 import QtWidgets


import formify
from formify import controls
from formify.layout import Row, Col, SidebarContentView, ensure_layout

from formify.tools import BackgroundMethod


class Window(QtWidgets.QDialog):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("My Window")

		plot = controls.ControlMatplotlib()

		fac = 0
		def factor():
			nonlocal fac
			fac += 1
			return fac

		def _draw(fig, factor):
			from time import sleep
			sleep(1)
			import numpy as np
			fig.clear()
			ax = fig.gca()
			x = np.linspace(0, 2 * np.pi)
			ax.plot(x, np.sin(x) * factor)

		draw = BackgroundMethod(_draw, cleanup=plot.canvas.draw, lazy=True)
		draw(plot.fig, 3)
		draw(plot.fig, 4)

		def toggle_toolbar():
			plot.toolbar_visible = not plot.toolbar_visible

		layout = ensure_layout(SidebarContentView({
			"Frickes": Col(
				plot,
				controls.ControlButton("Toggle Toolbar", on_click=toggle_toolbar),
				controls.ControlButton("Draw", on_click=lambda : draw(plot.fig, factor())),
			),
			"Ludolfs": Col(
				controls.ControlFloat("Hedwig"),
				controls.ControlRadio("Hedwig"),
				controls.ControlRadio("Hedwig"),
			),
			"Conditional": controls.ConditionalForm({
				"Condtion1": Row(controls.ControlCheckbox(variable_name="schlafen"), controls.ControlButton("Aufwachen")),
				"Condtion2": Row(controls.ControlButton("Nicht Schlafen")),
			}, on_change=print)
		}))
		layout.setMargin(0)

		self.setLayout(layout)


if __name__ == '__main__':
	# Create the Qt Application
	app = QtWidgets.QApplication(sys.argv)
	app.setStyleSheet(formify.stylesheet())

	form = Window()
	form.show()
	# Run the main Qt loop
	sys.exit(app.exec_())