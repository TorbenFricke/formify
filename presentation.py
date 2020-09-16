from formify.controls import *
from formify.layout import *
import formify

machine = Form(Col(
	ControlText(variable_name="machine_name"),
	Row(
		Col(
			ControlText(variable_name="material_name"),
			ControlFloat(variable_name="conductivity"),
			ControlFloat(variable_name="temperature"),
		),
		ControlTable(variable_name="bh", columns=["H", "B"]),
	),
))


command = ControlText(value="machine.value")
ui = Col(
	Segment(h2("Machine"), machine),
	Row(
		command,
		ControlButton("Evaluate", on_click=lambda : print(eval(command.value)))
	)
)

machine.change.subscribe(print)


formify.MainWindow(ui, margin=8)