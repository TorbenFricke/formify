import pathlib, os
from PySide6 import QtGui
from PySide6 import QtWidgets
import sys, typing
from formify import localization
from formify import _rember_ui_settings


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
		self.remember_ui_settings = _rember_ui_settings.UISaveLoad(self.get_ui_settings, app_name=self.name)
		ui_settings = self.remember_ui_settings.load()
		if ui_settings is not None:
			self.apply_ui_settings(ui_settings)
		self.splash: typing.Optional[QtWidgets.QSplashScreen] = None

	def get_ui_settings(self):
		"""
		Can be overridden to include other UI Settings. Will be loaded, as the app is created.
		Be sure to also override apply_ui_settings.

		"""
		return {
			"language": self.translator.language,
		}

	def apply_ui_settings(self, ui_settings: dict):
		"""
		Applies a ui_settings (dict). By default this us only the UI language. This is done, while formify is being
		imported, so before any UI components are created.
		"""
		self.translator.language = ui_settings["language"]

	def run(self):
		# close the pyinstaller spashscreen
		try:
			import pyi_splash
			pyi_splash.close()
		except ImportError:
			pass

		# hide splashscreen
		if self.splash is not None:
			self.splash.finish(self)
			self.splash.deleteLater()

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


def add_font(tff_file_name):
	QtGui.QFontDatabase.addApplicationFont(tff_file_name)


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
