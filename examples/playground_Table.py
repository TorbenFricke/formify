from formify import *
import typing
import formify


table = ControlTable(columns=["H", "B"], column_types=[bool, ("A", "B")])
table.change.subscribe(print)

def do_stuff():
	table.fixed_no_rows = 4


window = MainWindow(Col(
	table,
	ControlButton("Print", do_stuff)
), margin=8)


