from formify.layout import *
from formify.controls import *
import formify


def print_text():
	text = ui.value["text"]
	if ui.value["print_mode"] == "Dialog":
		formify.tools.ok_dialog("Text:", text)
	else:
		print(text)


def set_value():
	ui.value  = {'text': 'Moin GUI Runde ', 'print_mode': 'Dialog'}


ui = Form(Col(
	Row(
		ControlText(variable_name="text", value="Print this text"),
		ControlCombo("Mode", items=["Dialog", "Print"], variable_name="print_mode"),
	),
	ControlButton("print or show dialog", on_click=print_text),
))

menu = {
	"Print Menu": {
			"print / show dialog": (print_text, "ctrl+p")
	}
}


formify.MainWindow(ui, menu=menu, margin=8)