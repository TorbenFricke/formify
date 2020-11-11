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


def _formset_layout(layout, controls):
	layout.setMargin(0)
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
	layout.setMargin(0)
	n = len(controls)
	for i, control in enumerate(controls):
		layout.addWidget(ensure_widget(control))
		if i != n - 1:
			layout.addStretch(stretch)
	return layout


def Tabs(tabs_dict: dict) -> QtWidgets.QTabWidget:
	tabs = QtWidgets.QTabWidget()
	for label, content in tabs_dict.items():
		layout = ensure_layout(content)
		layout.setMargin(TAB_PADDING)
		tabs.addTab(
			ensure_widget(layout),
			label)
	return tabs


def Grid(*controls, columns=3):
	buckets = [[] for _ in range(columns)]
	for i, control in enumerate(controls):
		buckets[i % columns].append(control)

	return Row(
		*[Col(*bucket) for bucket in buckets]
	)


def SplitterRow(*args, collapsible=False, **kwargs):
	splitter = QtWidgets.QSplitter()
	splitter.setChildrenCollapsible(collapsible)
	for widget in args:
		splitter.addWidget(
			ensure_widget(widget)
		)

	return splitter


def SplitterCol(*args, **kwargs):
	splitter = SplitterRow(*args, **kwargs)
	splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
	return splitter


def ScrollArea(widget):
	area = QtWidgets.QScrollArea()
	area.setWidgetResizable(True)
	area.setWidget(widget)
	return area