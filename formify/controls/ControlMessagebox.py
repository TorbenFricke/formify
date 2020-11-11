from PySide2 import QtWidgets
import typing


class ControlMessagebox(QtWidgets.QMessageBox):
	def __init__(self, title="Sure?", text="Are you sure?"):
		QtWidgets.QMessageBox.__init__(self)

		self.setWindowTitle(title)
		self.setText(text)

		self.make_buttons()

	def make_buttons(self):
		self.setStandardButtons(self.Yes)
		self.addButton(self.No)
		self.setDefaultButton(self.No)

	def show(self, true_btn=QtWidgets.QMessageBox.Yes):
		return self.exec_() == true_btn
