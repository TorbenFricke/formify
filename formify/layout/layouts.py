import typing
from PySide2 import QtWidgets, QtCore
from formify.controls import ControlBase


TAB_PADDING = 5


def ensure_widget(layout_or_widget: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout]) -> QtWidgets.QWidget:
	if isinstance(layout_or_widget, QtWidgets.QWidget):
		return layout_or_widget
	widget = QtWidgets.QWidget()
	widget.setLayout(layout_or_widget)
	return widget


def ensure_layout(layout_or_widget: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout]) -> QtWidgets.QLayout:
	if isinstance(layout_or_widget, QtWidgets.QLayout):
		return layout_or_widget
	layout = QtWidgets.QVBoxLayout()
	layout.addWidget(layout_or_widget)
	return layout


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

def Row(*args, **kwargs) -> QtWidgets.QLayout:
	return _Row(*args, **kwargs).generate()


class _Column(BaseLayout):
	def _make_layout(self):
		layout = QtWidgets.QVBoxLayout()
		layout.setAlignment(QtCore.Qt.AlignTop)
		return layout

def Col(*args, **kwargs) -> QtWidgets.QLayout:
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
			return Col(_content)

		tabs = QtWidgets.QTabWidget(parent)
		for label, content in self.tabs_dict.items():
			layout = layout_box(content)
			layout.setMargin(TAB_PADDING)
			tabs.addTab(
				ensure_widget(layout),
				label)
		return tabs

def Tabs(*args, **kwargs) -> QtWidgets.QTabWidget:
	return _Tabs(*args, **kwargs).generate()


def Segment(layout_or_control, *args) -> QtWidgets.QWidget:
	widget = QtWidgets.QWidget()
	widget.setWhatsThis("segment")
	widget.setContentsMargins(7, 7, 7, 7)

	if isinstance(layout_or_control, QtWidgets.QLayout):
		widget.setLayout(layout_or_control)
	else:
		widget.setLayout(Col(
			layout_or_control,
			*args
		))
	return widget