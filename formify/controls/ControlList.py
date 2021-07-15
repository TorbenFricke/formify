from formify.controls import ControlBase, ControlButton
from formify.controls._list_base import ItemBase
from formify.layout import Row, ensure_widget
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
import typing

from formify.controls._events import EventDispatcher

def rearrange(some_list, r_from, r_to):
	#print(f"from {r_from} to {r_to}")
	some_list.insert(r_to, some_list.pop(r_from))
	return some_list

class ControlList(ControlBase, ItemBase):
	def __init__(self,
	             label: str = None,
	             variable_name: str = None,
	             value: typing.Any = None,
	             add_click: typing.Callable = None,
	             remove_click: typing.Callable = None,
	             items: list=None,
	             parent: QtWidgets.QWidget = None,
	             on_change: typing.Callable = None,
				 display_name_callback: callable = str,
	             rearrangeable:bool = True):

		# events
		self.add_click = add_click
		self.remove_click = self.removeCurrentItem
		if remove_click is not None:
			self.remove_click = remove_click
		self.index_change = EventDispatcher(self)
		# repaint on every index change. Otherwise, the selection somtimes does not show on macOs Catalina
		self.index_change.subscribe(self.repaint)

		ControlBase.__init__(
			self,
			label=label,
			variable_name=variable_name,
			value=value,
			parent=parent
		)

		ItemBase.__init__(self, items, display_name_callback=display_name_callback)
		self.change = self.items_change
		if on_change is not None:
			self.change.subscribe(on_change)

		self.rearrangeable = rearrangeable


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

		# set drag and drop stuff
		self.control.supportedDropActions = lambda : Qt.MoveAction
		self.control.setDragDropMode(self.control.InternalMove)
		self.control.setAcceptDrops(True)
		self.control.setDropIndicatorShown(True)

		def drop(event):
			if len(self.items) < 1:
				return False

			def find_row_from(bytearray):
				ds = QtCore.QDataStream(bytearray)
				return ds.readInt32()

			data = event.mimeData()
			x_abstract_list = 'application/x-qabstractitemmodeldatalist'
			if data.hasFormat(x_abstract_list):
				indices = find_row_from(data.data(x_abstract_list))
				row_from = indices

				row_to = self.control.indexFromItem(self.control.itemAt(event.pos())).row()
				if self.control.dropIndicatorPosition().name == b"BelowItem":
					row_to += 1

				if row_from < row_to:
					row_to -= 1

				if row_to == -1:
					return False

				with self.index_change.suspend_updates():
					self.items = rearrange(self.items, row_from, row_to)
				self.index = row_to
				self.control.repaint()

			return False

		self.control.dropEvent = drop

		yield self.control

		# make the _buttons
		def make_handler(func_name):
			def wrapped():
				# we have to get the function this way, as otherwise you
				# would not be able to set a different function later
				func = getattr(self, func_name)
				if func is None:
					return
				try:
					return func(self)
				except TypeError:
					pass
				return func()
			return wrapped
		self.add_button = ControlButton(app.translator("+ Add"), on_click=make_handler("add_click"))
		self.remove_button = ControlButton(app.translator("- Remove"), on_click=make_handler("remove_click"))
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
		def name_changed():
			if self.control.count() != len(display_names):
				return True
			# check if item changed
			for i, new_name in enumerate(display_names):
				current_name = self.control.item(i)
				if current_name != new_name:
					return True
			return False

		if not name_changed():
			return

		with self.index_change.suspend_updates():
			# remember index
			index = self.index

			# set new values
			self.control.clear()
			if len(display_names) > 0:
				self.control.addItems(display_names)

			# reset index
			self.index = index

	@property
	def value(self):
		return self.items


	@value.setter
	def value(self, value):
		self.items = value


	@property
	def rearrangeable(self):
		return self.control.dragEnabled()

	@rearrangeable.setter
	def rearrangeable(self, value):
		self.control.setDragEnabled(value)