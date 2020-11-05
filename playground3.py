import formify
from formify import controls, layout

_boop = controls.ControlText(variable_name="Boop", value="boop")

def boop():
	print(_boop.value)

sub_content = layout.Segment(
	controls.ControlCheckbox(variable_name="Box"),
	controls.ControlRadio(variable_name="Box2"),
	controls.ControlRadio(variable_name="Box3", on_change=print),
)


content = layout.Segment(
	layout.h1("Segment"),
	controls.ControlCheckbox(variable_name="Checkbox"),
	controls.ControlText(variable_name="Text"),
	controls.ControlTextarea("Bla", variable_name="TextArea", on_change=print),
	_boop,
	controls.ControlButton("Make Boop", on_click=boop),
	controls.ControlButton("Show Sub Window", on_click=lambda : sub_content.show()),
)

menu = {
	"Playground": {
		"Boop": (boop, "ctrl+b")
	}
}

formify.MainWindow(content, menu=menu, margin=8)