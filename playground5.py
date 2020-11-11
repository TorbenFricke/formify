import formify
from formify.controls import *
from formify.layout import *

content = Row(
	Col(
		ControlButton("Button 1"),
		ControlButton("Button 2"),
		ControlText("Button 2"),
		ControlButton("Button 2"),
	),
	ColSpaceBetween(
		ControlButton("Button 1"),
		ControlButton("Button 2"),
		ControlText("Button 2"),
		ControlButton("Button 2"),
	),
)

formify.MainWindow(content, margin=8)