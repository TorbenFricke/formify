from PySide2 import QtWidgets, QtCore
import typing
from formify.layout import Col, text, ensure_widget
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
				 display_name_callback=str,
				 top_widget: QtWidgets.QWidget=None,
				 bottom_widget: QtWidgets.QWidget=None):
		QtWidgets.QFrame.__init__(self)
		self._buttons: typing.List[SidebarButton] = []
		self.top_layout, self.btn_layout, self.bottom_layout = self._make_layout()

		if top_widget is not None:
			self.top_layout.addWidget(top_widget)
		if bottom_widget is not None:
			self.bottom_widget.addWidget(bottom_widget)

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

		btn = SidebarButton(text, click=make_set_checked(len(self._buttons)))
		self._buttons.append(btn)
		self.btn_layout.addWidget(btn)
		return btn

	def _make_layout(self):
		def tight_col(margin=0):
			_layout = QtWidgets.QVBoxLayout()
			_layout.setAlignment(QtCore.Qt.AlignTop)
			_layout.setMargin(0)
			_layout.setSpacing(0)
			_layout.setContentsMargins(margin, margin, margin, margin)
			return _layout

		bottom_layout
		# make the main layout
		layout = tight_col()
		self.setLayout(layout)

		# top layout
		top_layout = tight_col(margin=0)
		layout.addLayout(top_layout, 0)

		# button layout (with stretch)
		btn_layout = tight_col()
		layout.addLayout(btn_layout, 1)

		# bottom layout - add some stretch
		bottom_layout = tight_col(margin=0)
		layout.addLayout(bottom_layout, 0)

		return top_layout, btn_layout, bottom_layout

	def _update_checked_states(self):
		# set checked state on Push Buttons
		for i, btn in enumerate(self._buttons):
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

	def ensure_number_buttons(self, n):
		# correct number of _buttons
		if n == len(self._buttons):
			return
		# remove _buttons
		while n < len(self._buttons):
			btn = self.btn_layout.takeAt(n)
			self._buttons.pop(n)
			btn.widget().deleteLater()
		# add _buttons
		while n > len(self._buttons):
			self._make_button("")

	def set_display_names(self, display_names):
		self.ensure_number_buttons(len(display_names))
		for i, name in enumerate(display_names):
			self._buttons[i].label = name

	@property
	def value(self):
		return self.items[self.index]

	@value.setter
	def value(self, value):
		for i, item in enumerate(self.items):
			if item == value:
				self.index = i
