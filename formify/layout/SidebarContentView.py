from formify.layout import ConditionalLayout, Row
from PySide2 import QtWidgets
import typing

class SidebarContentView(QtWidgets.QWidget):
	def __init__(self, layouts: dict, value:str = None, sidebar_class=None):
		QtWidgets.QWidget.__init__(self)
		self.content = ConditionalLayout(layouts, visible=value)
		self.content.layout().setMargin(8)

		if sidebar_class is None:
			# import sidebar now to prevent circular imports
			from formify.controls import ControlSidebarLight
			sidebar_class = ControlSidebarLight
		self.sidebar = sidebar_class(list(layouts.keys()))

		self.setLayout(
			Row(self.sidebar, self.content)
		)

		def set_visible(index):
			self.content.visible = self.sidebar.items[index][0]

		self.sidebar.index_change.subscribe(
			lambda sender, index: set_visible(index)
		)
