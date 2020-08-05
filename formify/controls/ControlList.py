from formify.controls import ControlBase, ControlButton
from formify.layout import Row, ensure_widget
from PySide2 import QtWidgets
import typing

from formify.controls._mixins import ItemMixin
from formify.controls._events import EventDispatcher

class ControlList(ControlBase, ItemMixin):
	def __init__(self,
	             label: str = None,
	             variable_name: str = None,
	             value: typing.Any = None,
	             add_click: typing.Callable = None,
	             remove_click: typing.Callable = None,
	             items: list=None,
	             parent: QtWidgets.QWidget = None,
	             on_change: typing.Callable = None):

		# events
		self.add_click = add_click
		self.remove_click = self.removeCurrentItem
		if remove_click is not None:
			self.remove_click = remove_click
		self.index_change = EventDispatcher(self)
		# repaint on every index change. Otherwise, the selection somtimes does not show on macOs Catalina
		self.index_change.subscribe(self.repaint)

		ControlBase.__init__(self,
					    	 label=label,
		                     variable_name=variable_name,
		                     value=value,
		                     parent=parent,
		                     on_change=on_change)

		ItemMixin.__init__(self, items)
		self.change = EventDispatcher(self)
		self.items_change.subscribe(lambda: self.change())

	def removeCurrentItem(self):
		if len(self._items) == 0:
			return
		del self._items[self.index]
		self.items = self._items

	def _make_control_widgets(self) -> typing.List[QtWidgets.QWidget]:
		self.control = QtWidgets.QListWidget(parent=self)
		# set the on change handler
		self.control.itemSelectionChanged.connect(
			lambda: self.index_change(self.index)
		)

		yield self.control

		# make the buttons
		def make_handler(func_name):
			def wrapped():
				# we have to get the function this way, as otherwise you
				# would not be able to set a different function later
				func = getattr(self, func_name)
				if func is None:
					return
				try:
					func(self)
				except TypeError:
					func()
			return wrapped
		self.add_button = ControlButton("+ Add", on_click=make_handler("add_click"))
		self.remove_button = ControlButton("- Remove", on_click=make_handler("remove_click"))
		yield ensure_widget(Row(self.add_button, self.remove_button))

	@property
	def index(self) -> int:
		return self.control.currentRow()

	@index.setter
	def index(self, value: int):
		self.control.setCurrentRow(value)
		# if the current row is set to -1 no event is triggered automatically. So we do it manually
		if value == -1:
			self.index_change(value)

	def set_display_names(self, display_names):
		with self.index_change.suspend_updates():
			self.control.clear()
			if len(display_names) > 0:
				self.control.addItems(display_names)
			self.control.repaint()

	@property
	def value(self):
		return [value for value, _ in self.items]

	@value.setter
	def value(self, value):
		self.items = value