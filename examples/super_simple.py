from formify import *

items_dict = {"a": "a", "B": "b", "c": "c"}
items = ["a", "b", "c"]

combo = ControlList("ControlSelect", value=items)
combo.items_change.subscribe(print)
#combo.change.subscribe(print)
#combo.index_change.subscribe(print)

radio = ControlRadio(on_change=print)

def do_something():
    combo.items += ["Z"]
    radio.value = not radio.value
    #combo.value = "asd"

btn = ControlButton("Do Something", on_click=do_something)

MainWindow(Row(
    ControlSelectSidebar(["Hallo", "Welt"], on_change=print),
    Col(combo, radio, btn)
))