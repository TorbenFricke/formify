from formify.controls import ControlBase
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
import typing, io, csv
from formify.controls import ControlText, ControlFloat, ControlInt


# TODO fix . , issues

class ValidatorDelegate(QtWidgets.QItemDelegate):
	def __init__(self, parent, column_types:list=None):

		self.column_types = column_types

		self.current_value_mixin = None
		super().__init__(parent)

	def createEditor(self, parent, option, index):
		if self.column_types is None:
			cls = ControlText
		elif self.column_types[index.column()] is float:
			cls = ControlFloat
		elif self.column_types[index.column()] is int:
			cls = ControlInt
		else:
			cls = ControlText

		editor = cls("", parent=parent)
		editor.control.setParent(parent)
		self.current_value_mixin = editor
		return editor.control

	def setEditorData(self, editor, index):
		self.current_value_mixin.value = index.model().data(index, QtCore.Qt.EditRole)

	def setModelData(self, editor, model, index):
		model.setData(index, self.current_value_mixin.value, QtCore.Qt.EditRole)

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)


def table_item(text=""):
	item = QtGui.QStandardItem()
	item.setText(str(text))
	return item


class ControlTable(ControlBase):
	def __init__(
			self,
			columns: list,
			label: str = None,
			column_types:list=None,
			*args,
			**kwargs
	):
		self.column_types = column_types

		ControlBase.__init__(self,
		                     label,
		                     *args,
		                     **kwargs)

		self._columns = []
		self.columns = columns

		def ensure_empty_bottom_row():
			def add_row():
				row = self.model.rowCount()
				self.model.insertRow(row)
				for column in range(self.model.columnCount()):
					self.model.setItem(
						row,
						column,
						table_item()
					)

			def is_row_empty(row):
				for column in range(self.model.columnCount()):
					if self.data(row, column) != "":
						return False
				return True

			with self.change.suspend_updates():
				# no rows?
				if self.model.rowCount() == 0:
					add_row()
				# last row not empty?
				elif not is_row_empty(self.model.rowCount() - 1):
					add_row()
				# last row is empty?
				else:
					# multiple empty rows?
					while is_row_empty(self.model.rowCount() - 2):
						self.model.removeRow(self.model.rowCount() - 2)

		self.change.subscribe(ensure_empty_bottom_row)
		ensure_empty_bottom_row()


	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		def make_action(func, shortcut) -> QtGui.QAction:
			action = QtGui.QAction("", self.control, self)
			action.triggered.connect(func)
			action.setShortcut(shortcut)
			return action

		self.control = QtWidgets.QTableView(parent=self)
		self.model = QtGui.QStandardItemModel(parent=self)
		self.control.setModel(self.model)
		self.control.setItemDelegate(ValidatorDelegate(self, column_types=self.column_types))

		self.control.addAction(make_action(lambda: self.copy_selection(), QtGui.QKeySequence.Copy))
		self.control.addAction(make_action(lambda: self.paste_selection(), QtGui.QKeySequence.Paste))
		self.control.addAction(make_action(lambda: self.delete_selection(), QtGui.QKeySequence.Delete))
		self.control.addAction(
			make_action(lambda: self.delete_selection(), QtGui.QKeySequence(QtCore.Qt.Key_Backspace)))

		self.model.itemChanged.connect(lambda: self.change())

		return self.control

	def data(self, row, column):
		return self.model.data(self.model.index(row, column))

	def copy_selection(self):
		## source:
		# https://stackoverflow.com/questions/40225270/copy-paste-multiple-items-from-qtableview-in-pyqt4
		selection = self.control.selectedIndexes()
		if selection:
			rows = sorted(index.row() for index in selection)
			columns = sorted(index.column() for index in selection)
			rowcount = rows[-1] - rows[0] + 1
			colcount = columns[-1] - columns[0] + 1
			table = [[''] * colcount for _ in range(rowcount)]
			for index in selection:
				row = index.row() - rows[0]
				column = index.column() - columns[0]
				table[row][column] = index.data()

			# convert
			from formify import app
			app.clipboard().setText("\n".join(["\t".join(map(str, row)) for row in table]))

	def paste_selection(self):
		## source:
		# https://stackoverflow.com/questions/40225270/copy-paste-multiple-items-from-qtableview-in-pyqt4
		selection = self.control.selectedIndexes()
		if selection:
			model = self.control.model()

			from formify import app
			buffer = app.clipboard().text()
			rows = sorted(index.row() for index in selection)
			columns = sorted(index.column() for index in selection)
			reader = csv.reader(io.StringIO(buffer), delimiter='\t')
			if len(rows) == 1 and len(columns) == 1:
				for i, line in enumerate(reader):
					for j, cell in enumerate(line):
						cast = self.get_cast_function(columns[0] + j)
						model.setData(model.index(rows[0] + i, columns[0] + j), cast(cell))
			else:
				arr = [[cell for cell in row] for row in reader]
				for index in selection:
					row = index.row() - rows[0]
					column = index.column() - columns[0]
					cast = self.get_cast_function(index.column())
					model.setData(model.index(index.row(), index.column()), cast(arr[row][column]))

	def delete_selection(self):
		selection = self.control.selectedIndexes()
		model = self.control.model()
		if selection:
			with self.change.suspend_updates():
				for index in selection:
					model.setData(index, "")

			self.change()

	def get_cast_function(self, column: int):
		def _int(s) -> int:
			if s == "":
				return 0
			return int(s)

		def _float(s) -> float:
			if s == "":
				return 0
			if type(s) == str:
				return float(s.replace(",", "."))
			return float(s)

		known = {int: _int, float: _float}
		cast = str
		try:
			cast = self.column_types[column]
			if cast in known:
				cast = known[cast]
		finally:
			return cast

	def get_value(self):
		out = []
		for row in range(self.model.rowCount() - 1):
			out.append([])
			for column in range(self.model.columnCount()):
				cast = self.get_cast_function(column)
				out[-1].append(cast(self.data(row, column)))

		return out

	def set_value(self, value):
		n_rows = len(value)
		n_column = len(value[0]) if len(value) > 0 else 1
		self.model.setColumnCount(n_column)
		self.model.setRowCount(n_rows)

		with self.change.suspend_updates():
			for x in range(n_rows):
				for y in range(n_column):
					cast = self.get_cast_function(y)
					self.model.setItem(
						x,
						y,
						table_item(cast(value[x][y]))
					)
		self.change(value)

	@property
	def columns(self):
		return self._columns

	@columns.setter
	def columns(self, value):
		self._columns = value
		self.model.setColumnCount(len(value))
		for i, name in enumerate(value):
			item = QtGui.QStandardItem()
			item.setText(name)
			self.model.setHorizontalHeaderItem(i, item)
