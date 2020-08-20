from PySide2 import QtWidgets, QtGui
import formify, typing, json
from formify.controls import Form
import warnings

def ensure_form(thing: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form]) -> Form:
	if isinstance(thing, Form):
		return thing
	return Form(formify.layout.ensure_layout(thing))


class Window(QtWidgets.QDialog):
	def __init__(self,
	             layout_widget_form: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form],
	             title: str="",
	             margin=0,):
		super().__init__()
		self.setWindowTitle(title)

		self.form = ensure_form(layout_widget_form)
		layout = formify.layout.ensure_layout(self.form)
		layout.setMargin(margin)
		self.setLayout(layout)


def extract_file_name(dialog_return: tuple):
	file_name = dialog_return[0].url()
	# clean file name
	if file_name[:7] == "file://":
		file_name = file_name[7:]
	return file_name


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self,
	             layout_widget_form: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout, Form],
	             title: str="",
	             margin=0,
	             main_menu:dict=None,
	             auto_run=True,):
		super().__init__()

		self.setWindowTitle(title)

		self.form = ensure_form(layout_widget_form)
		self.form.layout().setMargin(margin)
		self.setCentralWidget(self.form)

		self.file_name: str = ""
		# make menu
		self.make_menu(main_menu)

		if auto_run:
			self.show()
			formify.run()

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


	def save(self):
		if self.file_name == "":
			self.save_as()
			return
		with open(self.file_name, "w+") as f:
			f.write(
				json.dumps(self.form.all_values, sort_keys=True, indent=4)
			)


	def save_as(self):
		self.file_name = extract_file_name(
			QtWidgets.QFileDialog(self).getSaveFileUrl(
				caption="Save as...",
			)
		)
		if self.file_name == "":
			return
		self.save()


	def open(self):
		self.file_name = extract_file_name(
			QtWidgets.QFileDialog(self).getOpenFileUrl(
				caption="Open...",
			)
		)
		if self.file_name == "":
			return
		with open(self.file_name) as f:
			s = f.read()
		try:
			self.form.all_values = json.loads(s)
		except Exception as e:
			warnings.warn(e)