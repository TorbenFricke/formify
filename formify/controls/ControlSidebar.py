from PySide2 import QtWidgets, QtCore
import typing
from formify.controls import ControlButton
from formify.controls._mixins import ItemMixin, ValueMixin
from formify.controls._events import EventDispatcher


class SidebarButton(QtWidgets.QPushButton):
	def __init__(self, label, checked=False, click=None):
		super().__init__()
		self.label = label
		self.checked = checked
		self.click = EventDispatcher(self)
		self.setCheckable(True)
		if click is not None:
			self.click.subscribe(click)
		# for some reason, the css styling breakes clicked.connect so we have to catch the mouse event manually
		self.mousePressEvent = lambda _ : self.click(self.checked)
		self.clicked.connect(lambda : self.click(self.checked))

	@property
	def label(self):
		return self.text()

	@label.setter
	def label(self, value):
		self.setText(value)

	@property
	def checked(self):
		return self.isChecked()

	@checked.setter
	def checked(self, value):
		self.setChecked(value)


class ControlSidebar(QtWidgets.QFrame, ItemMixin, ValueMixin):
	def __init__(self,
				 items:typing.List[str],
				 variable_name:str=None,
	             value:str=None,
				 on_change:typing.Callable=None,
				 display_name_callback=str):
		QtWidgets.QFrame.__init__(self)
		self.buttons: typing.List[SidebarButton] = []
		self._make_layout()

		# index change events
		self.index_change = EventDispatcher(self)
		self.index_change.subscribe(self._update_checked_states)

		self._index = -1
		ItemMixin.__init__(self, items, display_name_callback)
		self.index = 0

		ValueMixin.__init__(self, variable_name, value, on_change)


	def _make_button(self, text):
		def make_set_checked(idx):
			def wrapped():
				self.index = idx
			return wrapped

		btn = SidebarButton(text, click=make_set_checked(len(self.buttons)))
		self.buttons.append(btn)
		self.layout().addWidget(btn)
		return btn


	def _make_layout(self):
		# make layout
		layout = QtWidgets.QVBoxLayout()
		layout.setAlignment(QtCore.Qt.AlignTop)
		layout.setMargin(0)
		self.setLayout(layout)


	def _update_checked_states(self):
		# set checked state on Push Buttons
		for i, btn in enumerate(self.buttons):
			btn.checked = i == self._index


	@property
	def index(self) -> int:
		return self._index


	@index.setter
	def index(self, value: int):
		if value == self._index:
			self._update_checked_states()
			return
		self._index = value
		# cause event
		self.index_change(value)


	def set_display_names(self, display_names):
		def ensure_number_buttons(n):
			# correct number of buttons
			if n == len(self.buttons):
				return
			# remove buttons
			while n < len(self.buttons):
				btn = self.layout().takeAt(n)
				self.buttons.pop(n)
				btn.widget().deleteLater()
			# add buttons
			while n > len(self.buttons):
				self._make_button("")

		ensure_number_buttons(len(display_names))
		for i, name in enumerate(display_names):
			self.buttons[i].label = name


	@property
	def value(self):
		return self.items[self.index]

	@value.setter
	def value(self, value):
		for i, item in enumerate(self.items):
			if item == value:
				self.index = i
