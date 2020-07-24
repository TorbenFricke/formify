from PySide2 import QtWidgets
import typing

class ControlButton(QtWidgets.QPushButton):
	def __init__(self, text:str="", on_click:typing.Callable=None, **kwargs):
		super().__init__(text=text, **kwargs)
		self.on_click = on_click
		"""On Click handler. These two signatures work func(sender) or func()"""

		# try calling the on click function with the button object as sender
		def _on_click():
			if not callable(self.on_click):
				return
			try:
				self.on_click(self)
			except:
				self.on_click()

		self.clicked.connect(_on_click)
