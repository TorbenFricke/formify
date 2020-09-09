from formify.controls import ControlBase, ControlTree
from PySide2 import QtWidgets, QtCore
import typing
import formify


table = formify.controls.ControlTable(columns=["H", "B"])


window = formify.MainWindow(formify.layout.Col(
	table,
	formify.controls.ControlButton("Print", lambda : print(table.value))
), margin=8)


