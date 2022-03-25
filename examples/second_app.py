from formify import *


def reset_value():
    # set the values of our UI elements with variable names.
    # This works because we wrapped out UI in a "Form"
    ui.value = {'text': 'This will be printed!', 'print_mode': 'Dialog'}


def print_text():
    _text = ui.value["text"]
    if ui.value["print_mode"] == "Dialog":
        tools.ok_dialog("Title", _text)
    else:
        print(_text)


# Create a grid layout by nesting "Row" and "Col" as needed
# Wrap the layout in "Form" to enable querying: ui.value[text]
ui = Form(Col(
    Row(
        # provide variable names to enable save, load and autosave functionality as a JSON file
        ControlText(label="Output Text", variable_name="text", value="This will be printed!"),
        # if no label is provided, the variable name is treated as the name
        ControlSelect(items=["Dialog", "Print"], variable_name="print_mode"),
    ),
    ControlButton("print or show dialog", on_click=print_text),
))

# create the main menu as a dict
menu = {
    "Print Menu": {
        # The value can either be a tuple (callable, shortcut)
        # or just a callable
        "Print or Show Dialog": (print_text, "ctrl+p"),
        # If the key starts with "-" its treated as a separator.
        # The number of dashes does not matter.
        "-": None,
        "Reset Data": reset_value
    }
}

# create the main window. If you do not pass auto_run=False, the app launches.
MainWindow(ui, menu=menu, margin=8)
