from formify.layout import ConditionalLayout, Row
from PySide2 import QtWidgets
import typing

class SidebarContentView(QtWidgets.QWidget):
	def __init__(self, layouts: dict, value:str = None, **kwargs):
		QtWidgets.QWidget.__init__(self)
		self.content = ConditionalLayout(layouts, visible=value)
		self.content.layout().setMargin(8)

		from formify.controls import ControlSidebar
		self.sidebar = ControlSidebar(list(layouts.keys()), **kwargs)

		from formify.layout import ScrollArea
		self.setLayout(
			Row(self.sidebar, ScrollArea(self.content))
		)

		def set_visible(index):
			self.content.visible = self.sidebar.items[index]

		self.sidebar.index_change.subscribe(
			lambda sender, index: set_visible(index)
		)
