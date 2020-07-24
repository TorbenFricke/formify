import sys
from PySide2 import QtWidgets


import formify
from formify import controls
from formify.layout import Row, Column, Tabs

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

        btn1 = controls.ControlButton("boop", on_click=boop)
        btn2 = controls.ControlButton("change boop to beep", on_click=set_on_click)
        btns = (btn1, btn2)

        layout = Row(
            formify.layout.Sidebar(),
            Tabs({
                "something": Row(
                    controls.ControlText("changing", on_change=change),
                    controls.ControlText(on_change=change)
                ),
                "something else": Row(
                    controls.ControlInt(on_change=change),
                    controls.ControlInt(on_change=change),
                    controls.ControlFloatMega(on_change=change),
                ),
            }),
            Column(
                controls.ControlText(on_change=change),
                controls.ControlInt(),
                controls.ControlText(),
                *btns,
            ),
        ).generate()
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