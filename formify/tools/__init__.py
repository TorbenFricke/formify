from formify.tools.background_method import BackgroundMethod, Task, do_in_ui_thread
from formify.tools.relationship import Relationship
from formify.tools.file_dialogs import save_dialog, open_dialog
from PySide2 import QtWidgets


def maximize(widget) -> QtWidgets.QWidget:
	widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
	return widget