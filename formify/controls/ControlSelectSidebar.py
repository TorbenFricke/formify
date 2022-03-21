from PySide6 import QtWidgets, QtCore
import typing
from formify.controls._base import set_props
from formify.controls._value_base import ValueBase
from formify.controls._item_base import SelectBase
from formify.controls._events import EventDispatcher


class SidebarButton(QtWidgets.QPushButton):
	def __init__(self, label, checked=False, click=None):
		QtWidgets.QPushButton.__init__(self)
		self.label = label
		self.checked = checked
		self.click = EventDispatcher(self, always_fire=True)
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


class ControlSelectSidebar(QtWidgets.QFrame, SelectBase, ValueBase):
	def __init__(
			self,
			items:typing.List[str],
			variable_name: str = None,
			value: str = None,
			on_change: typing.Callable = None,
			display_name_callback = str,
			top_widget: QtWidgets.QWidget = None,
			bottom_widget: QtWidgets.QWidget = None,
			**kwargs
	):
		QtWidgets.QFrame.__init__(self)
		self._buttons: typing.List[SidebarButton] = []
		self.top_layout, self.btn_layout, self.bottom_layout = self._make_layout()

		if top_widget is not None:
			self.top_layout.addWidget(top_widget)
		if bottom_widget is not None:
			self.bottom_layout.addWidget(bottom_widget)

		self._index = -1

		ValueBase.__init__(self, variable_name, value=None, creat_change_event=False)
		SelectBase.__init__(self, items, display_name_callback)

		self.change = self.selected_item_change
		if on_change is not None:
			self.change.subscribe(on_change)

		self.value = value

		set_props(self, kwargs)

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
			_layout.setContentsMargins(margin, margin, margin, margin)
			return _layout

		# make the main layout
		layout = tight_col()
		self.setLayout(layout)

		# top layout
		top_layout = tight_col(margin=0)
		layout.addLayout(top_layout, 0)

		# button layout (with stretch)
		btn_layout = tight_col(margin=6)
		layout.addLayout(btn_layout, 1)

		# bottom layout - add some stretch
		bottom_layout = tight_col(margin=0)
		layout.addLayout(bottom_layout, 0)

		return top_layout, btn_layout, bottom_layout

	def _update_checked_states(self):
		# set checked state on Push Buttons
		for i, btn in enumerate(self._buttons):
			btn.checked = i == self._index

	def get_index(self) -> int:
		return self._index

	def set_index(self, index: int):
		if self._index != index:
			self._index = index
		self._update_checked_states()
		self.index_change(index)

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

	def get_value(self):
		return self.items[self.index]

	def set_value(self, value):
		for i, item in enumerate(self.items):
			if item != value:
				continue
			if i != self.index:
				self.index = i
				self.change(value)

