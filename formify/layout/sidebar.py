from PySide2 import QtWidgets, QtCore
from formify.controls import ControlButton


class Sidebar(QtWidgets.QFrame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.buttons = []
		self._checked = 0
		self.make_sidebar()
		self._update_checked()



	def make_sidebar(self):
		# make layout
		layout = QtWidgets.QVBoxLayout()
		layout.setAlignment(QtCore.Qt.AlignTop)
		layout.setMargin(0)

		def make_set_checked(idx):
			def wrapped():
				self.checked = idx
			return wrapped

		# set buttons
		words = ["Vats", "Horses", "Huge long text word words", "Elefant", "Tiger", "Cello"]
		for i, text in enumerate(words):
			btn = ControlButton(text)
			btn.setCheckable(True)
			btn.on_click = make_set_checked(i)
			self.buttons.append(btn)
			layout.addWidget(btn)

		self.setLayout(layout)


	def _update_checked(self):
		for i, btn in enumerate(self.buttons):
			btn.setChecked(i == self._checked)

	@property
	def checked(self):
		return self._checked

	@checked.setter
	def checked(self, value):
		self._checked = value
		self._update_checked()