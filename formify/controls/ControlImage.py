from PySide6 import QtWidgets, QtGui
from formify.controls._base import set_props


class ControlImage(QtWidgets.QLabel):
	def __init__(self, file_name: str = None, width=None, height=None, **kwargs):

		QtWidgets.QLabel.__init__(self)
		set_props(self, kwargs)

		self._file_name = file_name
		self._pixelmap = None
		self.set_image()
		self.width = width
		self.height = height


	def set_image(self):
		if self._file_name is not None:
			file_name = str(self._file_name)
			self._pixelmap = QtGui.QPixmap(file_name)
			self.setPixmap(self._pixelmap)

	def scale(self, w, h):
		if self._pixelmap is None:
			return
		self.setPixmap(
			self._pixelmap.scaled(w, h, QtGui.Qt.KeepAspectRatio)
		)

	@property
	def file_name(self) -> str:
		return self._file_name

	@file_name.setter
	def file_name(self, value: str):
		self._file_name = value
		self.set_image()

	@property
	def width(self):
		return super().width()

	@width.setter
	def width(self, value):
		if value is None:
			return
		self.scale(value, 100000)

	@property
	def height(self):
		return super().height()

	@height.setter
	def height(self, value):
		if value is None:
			return
		self.scale(100000, value)
