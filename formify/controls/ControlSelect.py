from formify.controls._item_base import SelectControlBase, ListControlBase
from formify.controls.ControlButton import ControlButton
from formify.layout.layouts import Row, ensure_widget
from PySide6 import QtWidgets
import typing


class ControlSelect(SelectControlBase):
	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change(self.control.currentIndex())
		)

		return self.control

	def get_index(self) -> int:
		return self.control.currentIndex()

	def set_index(self, index: int):
		self.control.setCurrentIndex(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		self.control.clear()
		self.control.addItems(display_names)


class ControlListDropdown(ListControlBase):
	def _make_control_widgets(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on index change handler
		self.control.currentIndexChanged.connect(
			lambda: self.index_change(self.control.currentIndex())
		)

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

		from formify import app

		self.add_button = ControlButton(app.translator("+ Add"), on_click=make_handler("add_click"))
		self.remove_button = ControlButton(app.translator("- Remove"), on_click=make_handler("remove_click"))
		yield ensure_widget(Row(self.add_button, self.remove_button))

	def get_index(self) -> int:
		return self.control.currentIndex()

	def set_index(self, index: int):
		self.control.setCurrentIndex(index)
		self.index_change(index)

	def set_display_names(self, display_names):
		# add items
		self.control.clear()
		self.control.addItems(display_names)

