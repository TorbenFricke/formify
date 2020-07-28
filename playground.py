import sys
from PySide2 import QtWidgets


import formify
from formify import controls
from formify.layout import Row, Col, Tabs, Segment, h5, h4, h3

def change(sender, value):
    print(f"{sender}: {value}")

def boop():
    print("boop")

def beep():
    print("beep")

def add_animal(sender):
    import random
    sender.items += [random.choice(["Cat", "Elefant", "Dog", "Horse", "Platypus", "Duck", "Chicken"])]

class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Form")

        def set_on_click():
            btn1.on_click = beep

        def set_form_data():
            conditional_form.value = some_form.value = {
                "microRotor": 10e-6,
                "microStator": 20e-6,
                "int": 123,
                "list": "two",
            }

        btn1 = controls.ControlButton("boop", on_click=boop)
        btn2 = controls.ControlButton("change boop to beep", on_click=set_on_click)
        btn3 = controls.ControlButton("set form data", on_click=set_form_data)
        btns = (btn1, btn2, btn3)

        some_form = controls.Form(Col(
            Segment(
                h3("Segment"),
                controls.ControlText("2 events", on_change=change, variable_name="2_changes"),
                controls.ControlInt(variable_name="int"),
                controls.ControlText(variable_name="text"),
            ),
            controls.ControlText("no event"),
            controls.ControlCombo("combo", items=["cat", ("dog", "Hund"), (1, "one")], variable_name="combo"),
            Tabs({
                "Stator": controls.ControlFloatMicro(variable_name="microStator"),
                "Rotor": controls.ControlFloatMicro(variable_name="microRotor"),
            }),
            *btns,
        ), on_change=change)

        conditional_form = controls.ConditionalForm({
            "v-pm": Col(
                controls.ControlText("changing", on_change=change),
                controls.ControlText(on_change=change),
                controls.ControlCheckbox("Include Losses", variable_name="checkbox_losses"),
                controls.ControlList("Some List", add_click=add_animal),
                btn1 = controls.ControlButton("boop", on_click=boop),
            ),
            "bar-pm": Col(
                Tabs({
                    "Stator": controls.ControlFloatMicro(variable_name="microStator"),
                    "Rotor": controls.ControlFloatMicro(variable_name="microRotor"),
                }),
                controls.ControlText(variable_name="text"),
            )
        }, variable_name="__flatten__")

        layout = Row(
            formify.layout.SidebarLight(),
            controls.Form(Col(
                conditional_form,
                controls.ControlInt(variable_name="another int"),
            ), on_change=change),
            some_form,
        )
        layout.setMargin(10)

        self.setLayout(layout)


if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(formify.stylesheet())

    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())