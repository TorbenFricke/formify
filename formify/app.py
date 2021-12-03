import pathlib, os
from PySide6 import QtGui
from PySide6 import QtWidgets
import sys
from formify import localization


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
		self.singe_instance = None
		self.translator = localization.default_translator()
		self.splash = None

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

	@property
	def allow_multiple_instances(self):
		return self.singe_instance is not None

	@allow_multiple_instances.setter
	def allow_multiple_instances(self, value):
		if value is True:
			del self.singe_instance
		else:
			from formify import tools

			if self.singe_instance is not None:
				return
			self.singe_instance = tools.SingleInstance(lambda : tools.ok_dialog(
				"Another Instance is Already Running",
				f"Another instance of {self.name} is already running. Exiting..."
			))


app = App()


def show_splashscreen(image_filepath: str = None):
	from PySide6.QtCore import Qt
	from PySide6.QtGui import QPixmap
	from PySide6.QtWidgets import QSplashScreen

	if image_filepath is None:
		image_filepath = str(pathlib.Path(__file__).parent / "splash.png")

	splash_image = QPixmap(image_filepath)

	app.splash = splash = QSplashScreen(splash_image, Qt.WindowStaysOnTopHint)
	splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
	splash.setEnabled(False)

	splash.show()
	app.processEvents()


def run():
	app.run()
