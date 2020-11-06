from PySide2 import QtWidgets, QtGui
import formify, typing, json
from formify.controls import Form
from formify.tools.file_dialogs import extract_file_name, save_dialog, open_dialog
import warnings

def ensure_form(thing: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form]) -> Form:
	if isinstance(thing, Form):
		return thing
	return Form(formify.layout.ensure_layout(thing))


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self,
	             layout_widget_form: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form],
	             title: str="",
	             margin=0,
	             width:int=None,
	             height:int=None,
	             menu:dict=None,
	             allowed_file_extensions=None,
	             auto_run=True,):
		super().__init__()

		self.allowed_file_extensions = allowed_file_extensions

		self.form = ensure_form(layout_widget_form)
		self.form.layout().setMargin(margin)
		self.setCentralWidget(self.form)

		if width is None:
			width = self.width()
		if height is None:
			height = self.height()
		self.resize(width, height)

		self._file_name: str = ""
		# make menu
		self.make_menu(menu)

		# set window title after file name
		self._title = ""
		self.title = title

		if auto_run:
			self.show()
			formify.run()


	@property
	def title(self):
		return self._title


	@title.setter
	def title(self, value):
		self._title = value
		self.update_window_title()


	@property
	def file_name(self):
		return self._file_name


	@file_name.setter
	def file_name(self, value):
		self._file_name = value
		self.update_window_title()


	def update_window_title(self):
		if self.title == "":
			self.setWindowTitle(f"{self.file_name}")
		else:
			self.setWindowTitle(f"{self.title} - {self.file_name}")


	def make_menu(self, menu_items: dict=None):
		def make_action(text, func, shortcut="") -> QtWidgets.QAction:
			action = QtWidgets.QAction(text, self)
			action.triggered.connect(func)
			if shortcut != "":
				action.setShortcut(
					QtGui.QKeySequence(shortcut)
				)
			return action

		def add_menus(menu, menu_items):
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
		key = "File"
		menu = menubar.addMenu(key)
		menu.addAction(make_action("Open...", self.open, "ctrl+o"))
		menu.addAction(make_action("Save...", self.save, "ctrl+s"))
		menu.addAction(make_action("Save As...", self.save_as, "ctrl+shift+s"))
		menu.addSeparator()

		add_menus(menu, menu_items.pop(key, {}))
		add_menus(menubar, menu_items)

	def file_extension_filter(self):
		if self.allowed_file_extensions is not None:
			return ";;".join([f"*.{ext}" for ext in self.allowed_file_extensions])
		else:
			return "*"

	def _save(self, file_name):
		with open(file_name, "w+") as f:
			f.write(
				json.dumps(self.form.all_values, indent=4)
			)

	def save(self):
		if self.file_name == "":
			self.save_as()
			return
		self._save(self.file_name)


	def save_as(self):
		self.file_name = save_dialog(title="Open...", filter=self.file_extension_filter())
		if self.file_name == "":
			return
		self.save()


	def _open(self, file_name):
		with open(file_name) as f:
			s = f.read()
		try:
			self.form.all_values = json.loads(s)
		except Exception as e:
			warnings.warn(e)


	def open(self):
		self.file_name = open_dialog(title="Open...", filter=self.file_extension_filter())
		if self.file_name == "":
			return
		self._open(self.file_name)