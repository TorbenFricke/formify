from formify.controls import ControlBase
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
import typing, io, csv
from formify.controls import ControlText, ControlFloat, ControlInt, ControlSelect
from formify.controls.ControlFloat import _str2float
from formify.controls.ControlInt import _str2int
from formify.controls._events import EventDispatcher
import formify


def _str2bool(s):
	if not isinstance(s, str):
		return bool(s)

	lower = s.lower()
	if lower in ["true", "x", "y", "yes"]:
		return True


class ValidatorDelegate(QtWidgets.QItemDelegate):
	def __init__(self, parent, column_types: list = None):
		self.column_types = column_types

		self.current_control = None
		super().__init__(parent)

	def createEditor(self, parent, option, index):
		if self.column_types is None:
			cls = ControlText
		elif self.column_types[index.column()] is float:
			cls = ControlFloat
		elif self.column_types[index.column()] is int:
			cls = ControlInt
		elif self.column_types[index.column()] is bool:
			return None
		elif type(self.column_types[index.column()]) is tuple:
			cls = ControlSelect
		else:
			cls = ControlText

		editor = cls("", parent=parent)
		editor.control.setParent(parent)
		if isinstance(editor, ControlSelect):
			editor.items = list(self.column_types[index.column()])
		self.current_control = editor
		return editor.control

	def setEditorData(self, editor, index):
		self.current_control.value = index.model().data(index, QtCore.Qt.EditRole)

	def setModelData(self, editor, model, index):
		model.setData(index, self.current_control.value, QtCore.Qt.EditRole)

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)
		editor.setStyleSheet("QLineEdit {border-radius: 0}")

	def destroyEditor(self, editor, index):
		self.current_control.deleteLater()
		del self.current_control
		self.current_control = None


def table_item(text=""):
	item = QtGui.QStandardItem()
	item.setText(str(text))
	return item


class TableUndoRedoCommand(QtGui.QUndoCommand):
	def __init__(self, old_value, new_value, table_view: 'ControlTable', *args, **kwargs):
		super().__init__()
		self.old_value = old_value
		self.new_value = new_value
		self.table_view = table_view

	def set(self, data):
		with self.table_view.undo_redo_event.suspend_updates():
			self.table_view.set_value(data)

	def undo(self):
		self.set(self.old_value)

	def redo(self):
		if self.table_view.undo_redo_event.suspend_update_count > 0:
			return
		self.set(self.new_value)


class ControlTable(ControlBase):
	def __init__(
			self,
			columns: list,
			label: str = None,
			column_types: list = None,
			column_widths: list = None,
			fixed_no_rows: int = None,
			*args,
			**kwargs
	):
		self.column_types = column_types

		ControlBase.__init__(
			self,
			label,
			*args,
			**kwargs
		)

		self.change.subscriptions.insert(0, self.ensure_no_rows)

		self._columns = []
		self.columns = columns

		self._fixed_no_rows = None
		self.fixed_no_rows = fixed_no_rows

		if column_widths is not None:
			for i, column_width in enumerate(column_widths):
				if column_width is None:
					continue
				self.control.setColumnWidth(i, column_width)

		self.undo_stack = QtGui.QUndoStack(self.control)
		self._prev_state = self.value

		def add_undo_item(_, value):
			new_state = value
			cmd = TableUndoRedoCommand(self._prev_state, new_state, self)
			# make sure not to run the redo command
			with self.undo_redo_event.suspend_updates():
				self.undo_stack.push(cmd)
			self._prev_state = new_state

		# this event will be triggered on every change, except when the chage was tiggered by an undo/redo
		self.undo_redo_event = EventDispatcher(None)
		self.undo_redo_event.subscribe(add_undo_item)
		self.change.subscribe(lambda _, value: self.undo_redo_event(value))

	def undo(self):
		self.undo_stack.undo()

	def redo(self):
		self.undo_stack.redo()

	def is_row_empty(self, row):
		for column in range(self.model.columnCount()):
			if self.is_bool_column(column):
				# not empty if the bool value has been set
				if self.data(row, column):
					return False
			elif self.data(row, column) != "":
				return False
		return True

	def add_row(self):
		row = self.model.rowCount()
		self.model.insertRow(row)
		for column in range(self.model.columnCount()):
			new_item = table_item()

			if self.is_bool_column(column):
				new_item.setCheckable(True)

			self.model.setItem(
				row,
				column,
				new_item
			)

	def ensure_no_rows(self):
		with self.change.suspend_updates():
			# fixed number of rows
			if self.fixed_no_rows is not None:
				while self.fixed_no_rows > self.model.rowCount():
					self.add_row()
				while self.fixed_no_rows < self.model.rowCount():
					self.model.removeRow(self.model.rowCount() - 1)
			# no rows?
			elif self.model.rowCount() == 0:
				self.add_row()
			# last row not empty?
			elif not self.is_row_empty(self.model.rowCount() - 1):
				self.add_row()
			# last row is empty?
			elif self.model.rowCount() >= 2:
				# multiple empty rows?
				while self.is_row_empty(self.model.rowCount() - 2):
					self.model.removeRow(self.model.rowCount() - 2)

	def _set_no_rows(self, no_rows):
		while no_rows > self.model.rowCount():
			self.add_row()
		while no_rows < self.model.rowCount():
			self.model.removeRow(self.model.rowCount() - 1)

	@property
	def fixed_no_rows(self):
		return self._fixed_no_rows

	@fixed_no_rows.setter
	def fixed_no_rows(self, value):
		prev = self._fixed_no_rows
		self._fixed_no_rows = value
		self.ensure_no_rows()
		if prev != value:
			self.change()

	def is_bool_column(self, column_index):
		if self.column_types is None:
			return False
		return len(self.column_types) > column_index and self.column_types[column_index] is bool

	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		def make_action(func, shortcut) -> QtGui.QAction:
			action = QtGui.QAction("", self.control, self)
			action.triggered.connect(func)
			action.setShortcut(shortcut)
			return action

		self.control = QtWidgets.QTableView(parent=self)
		self.model = QtGui.QStandardItemModel(parent=self)
		self.control.setModel(self.model)
		self.control.horizontalHeader().setStretchLastSection(True)
		self.control.setItemDelegate(ValidatorDelegate(self, column_types=self.column_types))

		self.control.addAction(make_action(lambda: self.undo(), QtGui.QKeySequence.Undo))
		self.control.addAction(make_action(lambda: self.redo(), QtGui.QKeySequence.Redo))
		self.control.addAction(make_action(lambda: self.cut_selection(), QtGui.QKeySequence.Cut))
		self.control.addAction(make_action(lambda: self.copy_selection(), QtGui.QKeySequence.Copy))
		self.control.addAction(make_action(lambda: self.paste_selection(), QtGui.QKeySequence.Paste))
		self.control.addAction(make_action(lambda: self.delete_selection(), QtGui.QKeySequence.Delete))
		self.control.addAction(
			make_action(lambda: self.delete_selection(), QtGui.QKeySequence(QtCore.Qt.Key_Backspace))
		)

		self.model.itemChanged.connect(lambda: self.change())

		return self.control

	def contextMenuEvent(self, event):
		def action(text):
			return menu.addAction(
				formify.app.translator(text)
			)

		menu = QtWidgets.QMenu(parent=self)
		undo = action("Undo")
		undo.setEnabled(self.undo_stack.canUndo())
		redo = action("Redo")
		redo.setEnabled(self.undo_stack.canRedo())
		menu.addSeparator()
		cut = action("Cut")
		copy = action("Copy")
		paste = action("Paste")
		delete = action("Delete")
		menu.addSeparator()
		select = action("Select All")
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == undo:
			self.undo()
		if action == redo:
			self.redo()
		if action == cut:
			self.cut_selection()
		elif action == copy:
			self.copy_selection()
		elif action == paste:
			self.paste_selection()
		elif action == delete:
			self.delete_selection()
		elif action == select:
			self.control.selectAll()

	def data(self, row, column):
		if self.is_bool_column(column):
			item = self.model.item(row, column)
			if item is None:
				return None
			return item.checkState() == Qt.CheckState.Checked
		return self.model.data(self.model.index(row, column))

	def set_data(self, row, column, data):
		cast = self.get_cast_function(column)
		if data is not None:
			casted = cast(data)
		else:
			casted = ""

		if self.is_bool_column(column):
			item = self.model.item(row, column)
			if item is None:
				return
			item.setCheckState(
				Qt.CheckState.Checked if casted else Qt.CheckState.Unchecked
			)
		else:
			self.model.setData(self.model.index(row, column), casted)

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
				table[row][column] = str(self.data(index.row(), index.column()))

			# convert
			from formify import app
			app.clipboard().setText("\n".join(["\t".join(map(str, row)) for row in table]))

	def paste_selection(self):
		## source:
		# https://stackoverflow.com/questions/40225270/copy-paste-multiple-items-from-qtableview-in-pyqt4
		selection = self.control.selectedIndexes()
		if not selection:
			return

		from formify import app
		buffer = app.clipboard().text()

		rows = sorted(index.row() for index in selection)
		columns = sorted(index.column() for index in selection)
		reader = csv.reader(io.StringIO(buffer), delimiter='\t')

		with self.change.suspend_updates():
			# only one cell selected
			if len(rows) == 1 and len(columns) == 1:
				for i, line in enumerate(reader):
					row = rows[0] + i

					# need new rows?
					if row >= self.model.rowCount():
						self.add_row()

					for j, cell in enumerate(line):
						column = columns[0] + j
						self.set_data(row, column, cell)

			else:
				arr = [[cell for cell in row] for row in reader]
				for index in selection:
					row = index.row() - rows[0]
					column = index.column() - columns[0]
					try:
						self.set_data(row, column, arr[row][column])
					except IndexError:
						break

			self.ensure_no_rows()

		self.change()

	def delete_selection(self):
		selection = self.control.selectedIndexes()
		if selection:
			with self.change.suspend_updates():
				for index in selection:
					self.set_data(index.row(), index.column(), None)

				self.ensure_no_rows()

			self.change()

	def delete_all(self):
		with self.change.suspend_updates():
			for row in range(self.model.rowCount()):
				for col in range(self.model.columnCount()):
					self.set_data(row, col, None)
			self.ensure_no_rows()
		self.change()

	def cut_selection(self):
		self.copy_selection()
		self.delete_selection()

	def get_cast_function(self, column: int):
		known = {int: _str2int, float: _str2float, bool: _str2bool}
		cast = str
		try:
			cast = self.column_types[column]
			if type(cast) is tuple:
				cast = lambda x: x
			if cast in known:
				cast = known[cast]
		finally:
			return cast

	def get_value(self):
		out = []
		n_rows = self.model.rowCount()
		for row in range(self.model.rowCount()):
			# break if last row is empty and we are not using fixed row numbers
			if self.fixed_no_rows is None and row == n_rows - 1 and self.is_row_empty(row):
				break

			out.append([])
			for column in range(self.model.columnCount()):
				cast = self.get_cast_function(column)
				out[-1].append(cast(self.data(row, column)))

		return out

	def set_value(self, value):
		# delete everything
		self.delete_all()

		if not value:
			return

		n_rows = len(value)
		n_column = len(value[0]) if len(value) > 0 else 1
		n_column_labels = len(self.columns)

		# only change the number of columns if no labels were set
		if n_column_labels == 0:
			self.model.setColumnCount(n_column)
		elif n_column > n_column_labels:
			n_column = n_column_labels

		with self.change.suspend_updates():
			if self.fixed_no_rows is not None:
				self._set_no_rows(self.fixed_no_rows)
				n_rows = self.fixed_no_rows
			else:
				self._set_no_rows(n_rows)

			for x in range(n_rows):
				for y in range(n_column):
					try:
						self.set_data(x, y, value[x][y])
					except IndexError:
						break
			self.ensure_no_rows()
		self.change(value)

	@property
	def columns(self):
		return self._columns

	@columns.setter
	def columns(self, value):
		#if self.column_types is not None:
		#	raise NotImplementedError("Cannot change columns if 'column_types' has been defined.")
		self._columns = value
		self.model.setColumnCount(len(value))
		for i, name in enumerate(value):
			item = QtGui.QStandardItem()
			item.setText(name)
			self.model.setHorizontalHeaderItem(i, item)
