import sys
from PySide2 import QtWidgets


import formify
from formify import controls
from formify.layout import Row, Col, Tabs, Segment, h5, h4, h3, SidebarContentView, ensure_layout


class Window(QtWidgets.QDialog):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("My Window")

		plot = controls.ControlMatplotlib()

		def toggle_toolbar():
			plot.toolbar_visible = not plot.toolbar_visible

		layout = ensure_layout(SidebarContentView({
			"Frickes": Col(
				plot,
				controls.ControlButton("Toggle Toolbar", on_click=toggle_toolbar),
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