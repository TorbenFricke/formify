from formify.layout import *
from formify.controls import *
import formify

formify.app.translator.language = "de"

ui = Form(Col(
	ControlCombo("Mode", items=[("German", "de"), ("English", "en")], variable_name="language"),
	ControlText("To be translated:", variable_name="translate"),
	ControlButton("Print Translation", on_click=lambda : print(translator(ui.value["translate"]))),
))

main_window = formify.MainWindow(ui, margin=8, auto_run=False)

main_window.show()
formify.app.run()