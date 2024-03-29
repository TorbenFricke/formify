import json
from formify import *

contact_info = Form(Col(
	ControlText("Phone Number", variable_name="phone"),
	ControlText("Email Address", variable_name="email"),
), variable_name="contact_info")


main_from = Form(Col(
	Row(
		ControlText("First Name", variable_name="first_name"),
		ControlText("Surname", variable_name="surname"),
	),
	ControlInt("Age", variable_name="age"),
	contact_info,
	ControlButton(
		"Print Value",
		on_click=lambda: print(json.dumps(main_from.value, indent=2))
	),
))

MainWindow(main_from, margin=9, title="Nested Values")
