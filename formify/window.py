from PySide6 import QtWidgets, QtGui
import formify, typing
from formify.controls import Form
from formify import LoadSaveHandler
import warnings

def ensure_form(thing: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form]) -> Form:
	if isinstance(thing, Form):
		return thing
	return Form(formify.layout.ensure_layout(thing))


class MainWindow(QtWidgets.QMainWindow):
	def __init__(
		self,
		layout_widget_form: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form],
		title: str = "",
		margin=0,
		width: int = None,
		icon_path: str = None,
		height: int = None,
		menu: dict = None,
		load_save_handler: LoadSaveHandler = None,
		allowed_file_extensions: list = None,
		auto_run=True
	):
		super().__init__()

		self.form = ensure_form(layout_widget_form)
		self.form.layout().setContentsMargins(margin,margin,margin,margin)
		self.setCentralWidget(self.form)

		# load save stuff
		if load_save_handler is None:
			load_save_handler = LoadSaveHandler(self.form)
		self.load_save_handler = load_save_handler
		if allowed_file_extensions is not None:
			self.load_save_handler.allowed_file_extensions = allowed_file_extensions

		# close event handler
		self.on_close = formify.controls.EventDispatcher(self)
		self.closeEvent = self.on_close
		self.on_close.subscribe(self.load_save_handler.autosave) # do an autosave if required

		if width is None:
			width = self.width()
		if height is None:
			height = self.height()
		self.resize(width, height)

		# make menu
		self.make_menu(menu)

		# set window title after file name
		self._title = ""
		self.title = title

		# update window title automatically
		self.load_save_handler.file_name_changed.subscribe(self.update_window_title)
		self.load_save_handler.no_changes_changed.subscribe(self.update_window_title)

		# icon
		if icon_path is not None:
			formify.app.set_icon(icon_path)

		# hide splashscreen
		if formify.app.splash is not None:
			formify.app.splash.finish(self)
			formify.app.splash.deleteLater()

		formify.app.main_window = self

		if auto_run:
			self.show()

			# run the app
			formify.run()

	@property
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value
		self.update_window_title()

	def update_window_title(self):
		title = self._title
		if self.load_save_handler.file_name != "":
			if title != "":
				title += " - "
			title += f"{self.load_save_handler.file_name}{'*' if self.load_save_handler.no_changes > 0 else ''}"
		title += self.load_save_handler.restored_label
		self.setWindowTitle(title)

	def make_menu(self, menu_items: dict=None):
		def add_menus(menu, menu_items):
			def make_action(text, func, shortcut="") -> QtGui.QAction:
				action = QtGui.QAction(text, menu)
				action.triggered.connect(func)
				if shortcut != "":
					action.setShortcut(
						QtGui.QKeySequence(shortcut)
					)
				return action

			for key, item in menu_items.items():
				# another sub menu
				if isinstance(item, dict):
					add_menus(menu.addMenu(key), item)
				# separators
				elif key.startswith("-"):
					menu.addSeparator()
				# actions with shortcut
				elif isinstance(item, tuple):
					menu.addAction(
						make_action(key, *item)
					)
				# action
				elif callable(item):
					menu.addAction(
						make_action(key, item)
					)
				else:
					warnings.warn(f"Unknown menu item type: {type(item)} - {item}")
		if menu_items is None:
			menu_items = {}

		menubar = self.menuBar()

		file_label = formify.app.translator("File")
		file_menu = menubar.addMenu(file_label)

		# load save menu
		add_menus(file_menu, self.load_save_handler.menu())
		file_menu.addSeparator()

		# user defined menus
		add_menus(file_menu, menu_items.pop(file_label, {}))
		add_menus(menubar, menu_items)