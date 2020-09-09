from formify.controls import ControlBase
from PySide2 import QtWidgets, QtGui, QtCore
import typing, io, csv



from formify.controls._mixins import ItemMixin

# TODO change item to model

def table_item(text=""):
	item = QtWidgets.QTableWidgetItem()
	item.setText(text)
	return item


class ControlTable(ControlBase):
	def __init__(self,
	             columns:list,
	             label:str=None,
	             items:list=None,
	             *args,
	             **kwargs):

		ControlBase.__init__(self,
		                     label,
		                     *args,
		                     **kwargs)

		self._columns = []
		self.columns = columns


		def ensure_empty_bottom_row():
			def add_row():
				row = self.control.rowCount()
				self.control.insertRow(row)
				for column in range(self.control.columnCount()):
					self.control.setItem(
						row,
						column,
						table_item()
					)

			def is_row_empty(row):
				for column in range(self.control.columnCount()):
					if self.control.item(row, column).text() != "":
						return False
				return True

			with self.change.suspend_updates():
				# no rows?
				if self.control.rowCount() == 0:
					add_row()
				# last row not empty?
				elif not is_row_empty(self.control.rowCount() - 1):
					add_row()
				# last row is empty?
				else:
					# multiple empty rows?
					while is_row_empty(self.control.rowCount() - 2):
						self.control.removeRow(self.control.rowCount() - 2)

		self.change.subscribe(ensure_empty_bottom_row)
		ensure_empty_bottom_row()


	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		def make_action(text, func, shortcut) -> QtWidgets.QAction:
			action = QtWidgets.QAction(text, self.control)
			action.triggered.connect(func)
			action.setShortcut(shortcut)
			return action

		self.control = QtWidgets.QTableWidget(parent=self)
		self.control.addAction(make_action("copy", lambda : self.copySelection(), QtGui.QKeySequence.Copy))
		self.control.addAction(make_action("paste", lambda : self.pasteSelection(), QtGui.QKeySequence.Paste))

		self.control.itemChanged.connect(lambda : self.change())

		return self.control


	def copySelection(self):
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
			app.clipboard().setText("\n".join(["\t".join(row) for row in table]))


	def pasteSelection(self):
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
						model.setData(model.index(rows[0] + i, columns[0] + j), cell)
			else:
				arr = [[cell for cell in row] for row in reader]
				for index in selection:
					row = index.row() - rows[0]
					column = index.column() - columns[0]
					model.setData(model.index(index.row(), index.column()), arr[row][column])


	@property
	def value(self):
		out = []
		for row in range(self.control.rowCount()):
			out.append([])
			for column in range(self.control.columnCount()):
				item = self.control.item(row, column)
				if item is None:
					out[-1].append(item)
				else:
					out[-1].append(item.text())
		return out


	@value.setter
	def value(self, value):
		n_rows = len(value)
		n_column = len(value[0])
		self.control.setColumnCount(n_column)
		self.control.setRowCount(n_rows)

		for x in range(n_rows):
			for y in range(n_column):
				self.control.setItem(
					x,
					y,
					table_item(value[x][y])
				)


	@property
	def columns(self):
		return self._columns

	@columns.setter
	def columns(self, value):
		self._columns = value
		self.control.setColumnCount(len(value))
		for i, name in enumerate(value):
			item = QtWidgets.QTableWidgetItem()
			item.setText(name)
			self.control.setHorizontalHeaderItem(i, item)
