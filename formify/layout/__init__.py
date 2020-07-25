import typing
from PySide2 import QtWidgets, QtCore
from formify.controls import ControlBase

from formify.layout.sidebar import Sidebar

TAB_PADDING = 5


def ensure_widget(layout_or_widget: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout]) -> QtWidgets.QWidget:
	if isinstance(layout_or_widget, QtWidgets.QWidget):
		return layout_or_widget
	widget = QtWidgets.QWidget()
	widget.setLayout(layout_or_widget)
	return widget


def add_layout_or_widget(parent, child):
	if isinstance(child, QtWidgets.QWidget):
		parent.addWidget(child)
	if isinstance(child, QtWidgets.QLayout):
		parent.addLayout(child)


class BaseLayout:
	def __init__(self, *args, **kwargs):
		self.kwargs = kwargs
		self.controls = args

	def _make_layout(self) -> QtWidgets.QLayout:
		return QtWidgets.QVBoxLayout()

	@staticmethod
	def formset_children(layout: QtWidgets.QLayout, controls, parent, children_controls):
		for item in controls:

			# another nested layout element
			if isinstance(item, QtWidgets.QLayout):
				layout.addWidget(ensure_widget(item))

			# a formify ControlBase
			elif isinstance(item, ControlBase):
				layout.addWidget(item)

			# a nested QWidget - For example a label
			# Note: The order is important, as sometimes Controls subclass ControlBase and QWidget.
			#       In these cases we want to execute the previous elif block.
			elif isinstance(item, QtWidgets.QWidget):
				layout.addWidget(item)

	def generate(self, parent=None, children_controls: list=None) -> typing.Union[QtWidgets.QLayout, QtWidgets.QWidget]:
		layout = self._make_layout()
		layout.setMargin(0)
		self.formset_children(layout, self.controls, parent=parent, children_controls=children_controls)
		return layout


class _Row(BaseLayout):
	def _make_layout(self):
		return QtWidgets.QHBoxLayout()

def row(*args, **kwargs):
	return _Row(*args, **kwargs).generate()


class _Column(BaseLayout):
	def _make_layout(self):
		layout = QtWidgets.QVBoxLayout()
		layout.setAlignment(QtCore.Qt.AlignTop)
		return layout

def col(*args, **kwargs):
	return _Column(*args, **kwargs).generate()

class _Tabs(BaseLayout):
	def __init__(self, tabs_dict: dict, **kwargs):
		BaseLayout.__init__(self, **kwargs)
		self.tabs_dict = tabs_dict

	def generate(self, parent=None, children_controls:list = None) -> QtWidgets.QWidget:
		def layout_box(_content):
			if isinstance(_content, QtWidgets.QLayout):
				return _content
			# make a Column containing the content
			return col(_content)

		tabs = QtWidgets.QTabWidget(parent)
		for label, content in self.tabs_dict.items():
			layout = layout_box(content)
			layout.setMargin(TAB_PADDING)
			tabs.addTab(
				ensure_widget(layout),
				label)
		return tabs

def tabs(*args, **kwargs):
	return _Tabs(*args, **kwargs).generate()
