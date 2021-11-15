from formify.controls import ControlBase
from PySide6 import QtWidgets, QtCore
import typing


def parents(tree_item):
	if tree_item is None or isinstance(tree_item, QtWidgets.QTreeWidget):
		return []
	parent = tree_item.parent()
	if parent is None:
		return []
	return parents(parent) + [parent]


def make_tree_item(text):
	_item = QtWidgets.QTreeWidgetItem()
	_item.setText(0, text)
	return _item


def dict_to_tree_items(d):
	items = []
	for key, value in d.items():
		items.append(make_tree_item(key))
		if isinstance(value, dict):
			items[-1].addChildren(
				dict_to_tree_items(value)
			)
	return items


class ControlTree(ControlBase):
	def __init__(
			self,
			label: str = None,
			variable_name: str = None,
			value: typing.Any = None,
			tree_data: dict=None,
			parent: QtWidgets.QWidget = None,
			on_change: typing.Callable = None
	):
		ControlBase.__init__(
			self,
			label=label,
			variable_name=variable_name,
			value=value,
			parent=parent,
			on_change=on_change,
		)

		self._tree_data = None
		self.tree_data = tree_data

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QTreeWidget()
		self.control.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

		self.control.currentChanged = lambda _, __: self.change()

		return self.control

	def get_item(self, path: list):
		if path is None: return None
		out = self.tree_data
		while len(path) > 0:
			out = out[path.pop(0)]
		return out

	@property
	def selected(self):
		return self.get_item(
			self.value
		)

	def get_value(self):
		try:
			_item = self.control.selectedItems()[0]
		except:
			return None
		return [node.text(0) for node in parents(_item)] + [_item.text(0)]

	def set_value(self, value):
		def find(items, txt):
			for item in items:
				if item.text(0) == txt:
					return item

		def walk(items, path):
			item = find(items, path[0])
			if item is None:
				raise ValueError(f"Could not set value of {self} to {value}")
			# last string in path?
			if len(path) == 1:
				return item
			else:
				return walk([item.child(i) for i in range(item.childCount())], path[1:])

		top_items = [self.control.topLevelItem(i) for i in range(self.control.topLevelItemCount())]

		# unselect old
		for selected in self.control.selectedItems():
			self.control.setItemSelected(selected, False)
		# select new
		self.control.setItemSelected(walk(top_items, value), True)

	@property
	def tree_data(self):
		return self._tree_data

	@tree_data.setter
	def tree_data(self, value):
		self._tree_data = value
		self.control.addTopLevelItems(dict_to_tree_items(value))
