from formify.tools.background_method import BackgroundMethod, Task, do_in_ui_thread
from formify.tools.relationship import Relationship
from formify.tools.file_dialogs import save_dialog, open_dialog
from formify.layout import ensure_widget
from PySide2 import QtWidgets


def maximize(widget) -> QtWidgets.QWidget:
	widget = ensure_widget(widget)
	widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
	return widget