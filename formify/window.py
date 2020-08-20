from PySide2 import QtWidgets
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
	             title: str="",):
		super().__init__()
		self.setWindowTitle(title)

		self.form = ensure_form(layout_widget_form)
		layout = formify.layout.ensure_layout(self.form)
		layout.setMargin(0)
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
	             main_menu:dict=None,):
		super().__init__()

		self.setWindowTitle(title)

		self.form = ensure_form(layout_widget_form)
		self.setCentralWidget(self.form)

		self.file_name: str = ""
		# make menu
		self.make_menu(main_menu)


	def make_menu(self, menu_items: dict=None):
		def make_action(text, func):
			action = QtWidgets.QAction(text, self)
			action.triggered.connect(func)
			return action

		def add_menus(menu, menu_items):
			for key, item in menu_items.items():
				# another sub menu
				if isinstance(item, dict):
					add_menus(menu.addMenu(key), item)
				# seperators
				elif key.startswith("-"):
					menu.addSeparator()
				# actions
				else:
					menu.addAction(
						make_action(key, item)
					)

		if menu_items is None:
			menu_items = {}

		menubar = self.menuBar()
		key = "File"
		menu = menubar.addMenu(key)
		menu.addAction(make_action("Open...", self.open))
		menu.addAction(make_action("Save...", self.save))
		menu.addAction(make_action("Save As...", self.save_as))
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
		with open(self.file_name) as f:
			s = f.read()
		try:
			self.form.all_values = json.loads(s)
		except Exception as e:
			warnings.warn(e)