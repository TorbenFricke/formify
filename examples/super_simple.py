from formify import *

show_splashscreen()
#import time
#time.sleep(2)
"""
QWidget {
    font-family: Helvetica,Arial,Font Awesome 6 Free;
}

"""

items_dict = {"a": "a", "B": "b", "c": "c"}
items = ["a", "b", "c"]

def add():
    combo.items += ["ads"]

combo = ControlListDropdown("ControlSelect", value=items, add_click=add)
combo.items_change.subscribe(print)
#combo.change.subscribe(print)
#combo.index_change.subscribe(print)

radios = SegmentAlt(Grid(
    *[ControlRadio(str(i), on_change=print) for i in range(12)],
    columns=4
))

def do_something():
    combo.items += ["Z"]
    #combo.value = "asd"

btn = ControlButton("Do Something", on_click=do_something)

table = ControlTable(columns=["B", "H", "Comment"], column_types=[bool, float, str])


def icon(title: str, *lines: str):
    _icon = SegmentAlt(
        h1(title),
        *[text(line) for line in lines]
    )

    # center text
    _icon.layout().setAlignment(QtCore.Qt.AlignJustify)
    for label in _icon.children():
        label.setAlignment(QtCore.Qt.AlignCenter)

    return SegmentSidebar(_icon)


MainWindow(SidebarContentView({
    "Table": Row(table, ControlTable(columns=["A", "B"])),
    "Hello": Segment(combo, radios, btn, ControlFile()),
    "World": Tabs({
        "Cat": Col(
            ControlFloat("Cat"),
            SegmentRed(text("dasads")),
            SegmentGreen(text("dasads")),
            SegmentBlue(text("dasads")),
            SegmentYellow(text("dasads")),
            SegmentPurple(text("dasads")),
            mute("dasads"),
        ),
        "Dog": ListForm(Form(Col(ControlFloat(variable_name="ads"), ControlInt(), ControlSelectRadio(items=["A", "B", "C"])))),
    })
},
    bottom_widget=icon("MyGui", "Version: 1.3", "Build: 4122"),
), title="Super Simple")