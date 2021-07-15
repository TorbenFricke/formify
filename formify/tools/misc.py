from formify.layout import ensure_widget
from PySide6 import QtWidgets
import os
import platform
import subprocess


def maximize(widget) -> QtWidgets.QWidget:
	widget = ensure_widget(widget)
	widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
	return widget


def disable_all_variables(widget):
	# import here to prevent circular imports
	from formify.controls import ValueBase, Form, ListForm

	for child in widget.children():

		# not a widget
		if not isinstance(child, QtWidgets.QWidget):
			continue

		# all normal controls
		if isinstance(child, ValueBase) and not isinstance(child, Form):
			if child.variable_name:
				child.setEnabled(False)

		# hide add and remove _buttons on list control
		if isinstance(child, ListForm):
			child.control.add_button.hide()
			child.control.remove_button.hide()

		disable_all_variables(child)


def open_file(path):
	if platform.system() == "Windows":
		os.startfile(path)
	elif platform.system() == "Darwin":
		subprocess.Popen(["open", path])
	else:
		subprocess.Popen(["xdg-open", path])