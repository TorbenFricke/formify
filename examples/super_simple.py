from formify import *

items_dict = {"a": "a", "B": "b", "c": "c"}
items = ["a", "b", "c"]

combo = ControlCombo(items=items)
combo.items_change.subscribe(print)
combo.change.subscribe(print)
combo.index_change.subscribe(print)

def do_something():
    combo.items = ["x", "y", "b", "z"]

btn = ControlButton("Do Something", on_click=do_something)

MainWindow(Col(combo, btn))