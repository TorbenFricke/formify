import sys
from PySide2 import QtWidgets


import formify
from formify import controls
from formify.layout import row, col, tabs

def change(sender, value):
    print(f"{sender}: {value}")

def boop():
    print("boop")

def beep():
    print("beep")


class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Form")

        def set_on_click():
            btn1.on_click = beep

        def set_form_data():
            some_form.value = {
                "microRotor": 10e-6,
                "microStator": 20e-6,
                "int": 123,
            }

        btn1 = controls.ControlButton("boop", on_click=boop)
        btn2 = controls.ControlButton("change boop to beep", on_click=set_on_click)
        btn3 = controls.ControlButton("set form data", on_click=set_form_data)
        btns = (btn1, btn2, btn3)

        some_form = controls.Form(col(
            controls.ControlText("2 events", on_change=change, variable_name="2_changes"),
            controls.ControlInt(variable_name="int"),
            controls.ControlText(variable_name="text"),
            controls.ControlText("no event"),
            tabs({
                "Stator": controls.ControlFloatMicro(variable_name="microStator"),
                "Rotor": controls.ControlFloatMicro(variable_name="microRotor"),
            }),
            *btns,
        ), on_change=change)


        layout = row(
            formify.layout.Sidebar(),
            tabs({
                "something": row(
                    controls.ControlText("changing", on_change=change),
                    controls.ControlText(on_change=change)
                ),
                "something else": row(
                    controls.ControlInt(on_change=change),
                    controls.ControlInt(on_change=change),
                    controls.ControlFloatMega(on_change=change),
                ),
            }),
            some_form,
        )
        layout.setMargin(10)

        self.setLayout(layout)


import qdarkstyle
print(qdarkstyle)

if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    app.setStyleSheet(formify.stylesheet())

    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())