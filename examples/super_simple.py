from formify import *

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

table = ControlTable(["B", "H", "Comment"], column_types=[float, float, str])


def icon(title: str, *lines: str):
    _icon = Segment(
        h1(title),
        *[mute(line) for line in lines]
    )

    # center text
    _icon.layout().setAlignment(QtCore.Qt.AlignJustify)
    for label in _icon.children():
        label.setAlignment(QtCore.Qt.AlignCenter)

    return SegmentSidebar(_icon)


MainWindow(SidebarContentView({
    "Hello": Segment(combo, radios, btn),
    "World": Tabs({
        "Cat": ControlFloat("Cat"),
        "Dog": ControlButton("Dog"),
    }),
    "Table": table,
},
    bottom_widget=icon("MyGui", "Version: 1.3", "Build: 4122"),
))