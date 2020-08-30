import formify
from formify import controls, layout


from PySide2 import QtWidgets, QtCore
qt_form_test = QtWidgets.QFormLayout()
qt_form_test.setLabelAlignment(QtCore.Qt.AlignLeft)
qt_form_test.setFormAlignment(QtCore.Qt.AlignLeft)
qt_form_test.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
qt_form_test.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
qt_form_test.setMargin(0)

qt_form_test.addRow("From Checkbox", controls.ControlCheckbox(variable_name="FormCheckbox"))
qt_form_test.addWidget(controls.ControlRadio(variable_name="Form Radio 1"))
qt_form_test.addWidget(controls.ControlRadio(variable_name="Form Radio 2"))
qt_form_test.addRow("Another Form Label", controls.ControlText(variable_name="Text"))
qt_form_test.addRow("Button", controls.ControlButton("Boop"))
#qt_form_test.addItem("Button", controls.ControlText(variable_name="Button"))


formify.MainWindow(layout.Segment(
	layout.h2("Qt From Test"),
	qt_form_test,
), margin=8)