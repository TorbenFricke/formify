from formify.controls import ControlBase, ControlTree
from PySide2 import QtWidgets, QtCore
import typing
import formify

def walk_children(root: QtWidgets.QWidget):
	def key(child):
		try:
			k = f"{child.variable_name} - {str(child)}"
		except:
			k = str(child)
		return k

	if not isinstance(root, QtWidgets.QWidget) and not isinstance(root, QtWidgets.QLayout):
		return root

	return {
		key(child): walk_children(child) for child in root.children()
		if not isinstance(child, QtWidgets.QLayout) # do not show layouts
	}


def highlight_control(c: QtWidgets.QWidget):
	try:
		c.setFocus()
	except:
		pass

class Inspector(QtWidgets.QWidget):
	def __init__(self, form: formify.controls.Form, parent=None):
		super().__init__(parent)

		self.tree = formify.controls.ControlTree(
			tree_data=walk_children(form),
		)
		self.tree.change.subscribe(
			lambda : highlight_control(self.tree.selected)
		)

		self.setLayout(formify.layout.Row(self.tree))


from formify import controls, layout
some_control = controls.ControlText(variable_name="some control")
content = layout.Segment(
	layout.h1("Segment"),
	controls.ControlCheckbox(variable_name="Checkbox"),
	controls.ControlText(variable_name="Text"),
	some_control,
	controls.ControlButton("Make Boop"),
	controls.ControlButton("Show Inspector", on_click=lambda : inspector.show()),
	controls.ControlButton("Hide Some Control", on_click=lambda : highlight_control(some_control)),
)
content = controls.Form(content)
inspector = Inspector(content)


#window = formify.MainWindow(content, margin=8)


master_dict = {
	"Top": "level",
	"Top 2": {
		"Child 1": "boop",
		"Child 2": {
			"Child Child": "boop child child"
		},
	},
}

tree = ControlTree(tree_data=master_dict)
tree.value = ["Top 2", "Child 1"]
tree.value = ["Top"]
print(tree.value)


window = formify.MainWindow(tree, margin=8)


