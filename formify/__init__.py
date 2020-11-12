from formify import controls, layout, tools
from formify.SaveLoad import LoadSaveHandler
from formify.window import MainWindow
from PySide2 import QtGui

import pathlib, os

stylesheet_root = pathlib.Path(__file__).parent

def stylesheet() -> str:
	def read(css_file):
		with open(str(stylesheet_root / css_file), "r") as f:
			return f.read()

	css = read("style.css")
	css += "\n"

	# windows
	if os.name == "nt":
		css += read("windows.css")

	return css

from PySide2 import QtWidgets
import sys

def _generate_appname():
	name = "formify"
	try:
		import __main__
		name += "-" + os.path.basename(__main__.__file__)
	except:
		pass
	return name

class App(QtWidgets.QApplication):
	def __init__(self, css=""):
		super().__init__(sys.argv)
		self.setStyleSheet(f"{stylesheet()}\n{css}")
		self.name = _generate_appname()

	def run(self):
		# Run the main Qt loop
		sys.exit(self.exec_())

	def setIcon(self, icon: str, window):
		_icon = QtGui.QIcon(icon)
		self.setWindowIcon(_icon)
		# windows
		if os.name == "nt":
			import ctypes
			myappid = icon  # arbitrary string
			ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


app = App()

def run():
	app.run()
