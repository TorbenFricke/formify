from formify import controls, layout, tools
from formify.window import MainWindow

import pathlib

stylesheet_root = pathlib.Path(__file__).parent

def stylesheet() -> str:
	def read(css_file):
		with open(str(stylesheet_root / css_file), "r") as f:
			return f.read()

	css = read("style.css")
	css += "\n"

	# platform specific css
	import os
	# windows
	if os.name == "nt":
		css += read("windows.css")

	return css

from PySide2 import QtWidgets
import sys


class App(QtWidgets.QApplication):
	def __init__(self, css=""):
		super().__init__(sys.argv)
		self.setStyleSheet(f"{stylesheet()}\n{css}")

	def run(self):
		# Run the main Qt loop
		sys.exit(self.exec_())

app = App()

def run():
	app.run()
