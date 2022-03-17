from PySide6 import QtWidgets
from formify.controls._base import set_props


class ControlMessagebox(QtWidgets.QMessageBox):
	def __init__(self, title="Sure?", text="Are you sure?", **kwargs):
		QtWidgets.QMessageBox.__init__(self)

		self.setWindowTitle(title)
		self.setText(text)

		self.make_buttons()

		set_props(self, kwargs)

	def make_buttons(self):
		self.setStandardButtons(self.Yes)
		self.addButton(self.No)
		self.setDefaultButton(self.No)

	def show(self, true_btn=QtWidgets.QMessageBox.Yes):
		return self.exec_() == true_btn
