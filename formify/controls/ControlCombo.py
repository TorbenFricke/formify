from formify.controls import ControlBase
from PySide2 import QtWidgets
import typing


class ControlCombo(ControlBase):
	def __init__(self,
	             label:str=None,
	             items:list=None,
	             *args,
	             **kwargs):
		# normalize items array
		def key_value(_items):
			for item in _items:
				if type(item) == str:
					yield item, item
				else:
					yield item[0], item[1]
		self._items = list(key_value(items))

		super().__init__(label,
		                 *args,
		                 **kwargs)


	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# add items
		for key, display_name in self._items:
			self.control.addItem(display_name)
		if len(self._items) > 0:
			self.control.setCurrentIndex(0)

		# set the on change handler
		self.control.currentTextChanged.connect(
			lambda: self._on_change()
		)

		return self.control

	@property
	def value(self):
		return self._items[self.control.currentIndex()][0]

	@value.setter
	def value(self, value):
		self.control.setCurrentText(value)
