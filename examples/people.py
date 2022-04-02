from formify import *
app.translator.language = "en"

# Option 1: A list form with a person form
person_form = Form(Col(
	ControlText("First Name", variable_name="first_name"),
	ControlText("Surname", variable_name="surname"),
	ControlText("Phone Number", variable_name="phone"),
	ControlInt("Age", variable_name="age"),
	ControlSelect("Role", items=["User", "Admin"], variable_name="role", value="User")
))

ui_list = ListForm(
	person_form,
	variable_name="people",
	display_name_callback=lambda person: f"{person['first_name']} {person['surname']} - {person['role']}"
)

# Option 2: A table
ui_table = ControlTable(
	label="",
	columns=["First Name", "Surname", "Phone Number", "Age", "Role"],
	column_types=[str, str, str, int, ("User", "Admin")],
	variable_name="people_table"
)

ui = SidebarContentView({
	"ListForm": ui_list,
	"Table": ui_table,
})

MainWindow(ui)