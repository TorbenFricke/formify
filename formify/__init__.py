from formify import controls, layout, tools
from formify.window import MainWindow

import pathlib

stylesheet_path = str(pathlib.Path(__file__).parent / "style.css")

def stylesheet() -> str:
	with open(stylesheet_path, "r") as f:
		return f.read()

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
