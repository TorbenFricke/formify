from formify.layout import *
from formify.controls import *
import formify

import geometry, model, material, results

js_text = text("")
calculation_window = Form(
	Col(
		h1("Calculation could be started now"),
		ScrollArea(js_text),
	)
)
calculation_window.layout().setMargin(12)

import json
def start_calculation():
	js_text.setText(json.dumps({
		key: value for key, value in main_view.value.items() if key in ["model", "singleload", "material"]
	}, indent=4))
	calculation_window.show()

main_view = Form(SidebarContentView({
	"Machine": Col(
		Tabs({
			"General": geometry.ui(),
			"Model": model.ui(),
		}),
		Row(
			ControlButton("Start Calculation", on_click=start_calculation),
			ControlButton("Print Value", on_click=lambda : print(json.dumps(main_view.value, indent=4))),
			ControlButton("Print All Values", on_click=lambda : print(json.dumps(main_view.all_values, indent=4))),
		),
	),
	"Materials": material.ui(),
	"Results": results.ui(),
}))


menu = {
	"File": {
		"Start Calculation...": (start_calculation, "ctrl+b")
	}
}


formify.MainWindow(main_view, menu=menu, title="SYMKO", margin=0)
