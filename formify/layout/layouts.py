import typing
from PySide6 import QtWidgets, QtCore
from formify.controls._base import set_props


# the windows default padding
TAB_PADDING = 9


# used for css styling of Columns/rows
class LayoutWidget(QtWidgets.QWidget): pass


def ensure_widget(layout_or_widget: typing.Union[QtWidgets.QWidget, QtWidgets.QLayout]) -> QtWidgets.QWidget:
	if isinstance(layout_or_widget, QtWidgets.QWidget):
		return layout_or_widget
	widget = LayoutWidget()
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


def _formset_layout(layout, controls):
	layout.setContentsMargins(0,0,0,0)
	for control in controls:
		layout.addWidget(ensure_widget(control))
	return layout

def Row(*controls) -> QtWidgets.QLayout:
	layout = QtWidgets.QHBoxLayout()
	_formset_layout(layout, controls)
	return layout


def Col(*controls) -> QtWidgets.QLayout:
	layout = QtWidgets.QVBoxLayout()
	_formset_layout(layout, controls)
	layout.setAlignment(QtCore.Qt.AlignTop)
	return layout


def ColSpaceBetween(*controls, stretch=1) -> QtWidgets.QLayout:
	layout = QtWidgets.QVBoxLayout()
	layout.setContentsMargins(0,0,0,0)
	n = len(controls)
	for i, control in enumerate(controls):
		layout.addWidget(ensure_widget(control))
		if i != n - 1:
			layout.addStretch(stretch)
	return layout


def Tabs(
		tabs_dict: dict,
		padding_left=TAB_PADDING,
		padding_top=TAB_PADDING,
		padding_right=TAB_PADDING,
		padding_bottom=TAB_PADDING
) -> QtWidgets.QTabWidget:

	tabs = QtWidgets.QTabWidget()
	for label, content in tabs_dict.items():
		layout = ensure_layout(content)
		layout.setContentsMargins(padding_left, padding_top, padding_right, padding_bottom)
		tabs.addTab(
			ensure_widget(layout),
			label
		)
	return tabs


def _Grid(*controls, columns=3):
	buckets = [[] for _ in range(columns)]
	for i, control in enumerate(controls):
		buckets[i % columns].append(control)

	return Row(
		*[Col(*bucket) for bucket in buckets]
	)


def Grid(*controls, columns=3):
	grid = QtWidgets.QGridLayout()
	grid.setContentsMargins(0, 0, 0, 0)

	for i, control in enumerate(controls):
		grid.addWidget(
			control,
			i // columns,
			i % columns,
		)

	return grid


def _setup_splitter(splitter, controls, collapsible, kwargs):
	splitter.setHandleWidth(2)
	splitter.setChildrenCollapsible(collapsible)
	for widget in controls:
		splitter.addWidget(
			ensure_widget(widget)
		)
	set_props(splitter, kwargs)


class SplitterRow(QtWidgets.QSplitter):
	def __init__(
			self,
			*controls,
			collapsible=False,
			**kwargs,
	):
		QtWidgets.QSplitter.__init__(self)
		_setup_splitter(self, controls, collapsible, kwargs)


class SplitterCol(QtWidgets.QSplitter):
	def __init__(
			self,
			*controls,
			collapsible=False,
			**kwargs,
	):
		QtWidgets.QSplitter.__init__(self)
		self.setOrientation(QtCore.Qt.Orientation.Vertical)
		_setup_splitter(self, controls, collapsible, kwargs)


def ScrollArea(widget, **kwargs):
	area = QtWidgets.QScrollArea()
	area.setWidgetResizable(True)
	area.setWidget(widget)
	set_props(area, kwargs)
	return area


class HLine(QtWidgets.QFrame):
	def __init__(self, **kwargs):
		super(HLine, self).__init__()
		self.setFrameShape(QtWidgets.QFrame.HLine)
		set_props(self, kwargs)


class VLine(QtWidgets.QFrame):
	def __init__(self, **kwargs):
		super(VLine, self).__init__()
		self.setFrameShape(QtWidgets.QFrame.VLine)
		set_props(self, kwargs)


class Placeholder(QtWidgets.QFrame):
	def __init__(self, width=0, height=0, **kwargs):
		super(Placeholder, self).__init__()
		set_props(self, kwargs)
		self.setFixedWidth(width)
		self.setFixedHeight(height)