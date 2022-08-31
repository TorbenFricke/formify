from formify import app
app.translator.language = "en"

import json
from formify import *

contact_info = Form(Col(
	ControlText("Kind", variable_name="contact_kind"),
	ControlText("Phone Number", variable_name="phone"),
	ControlText("Email Address", variable_name="email"),
))

contact_info_list = ListForm(
	model_form=contact_info,
	variable_name="contact_info",
	#display_name_callback=lambda x: x["contact_kind"],
)

main_from = Form(Col(
	Row(
		ControlText("First Name", variable_name="first_name"),
		ControlText("Surname", variable_name="surname"),
	),
	ControlInt("Age", variable_name="age"),
	contact_info_list,
	ControlButton(
		"Print Value",
		on_click=lambda: print(json.dumps(main_from.value, indent=2))
	),
))

MainWindow(main_from, margin=9, title="List Form")
