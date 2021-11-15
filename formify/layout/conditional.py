from formify.layout import Col, ensure_widget
from PySide6 import QtWidgets


class ConditionalLayout(QtWidgets.QWidget):
	def __init__(self, layouts:dict, visible: str = None):
		super().__init__()
		self.layouts = layouts

		self._conditional_panels = self._generate_panels()

		# the global layout, everything gets put into
		self.setLayout(Col(
			*list(self._conditional_panels.values()),
		))

		self._visible = ""
		if visible is None:
			self.visible = list(layouts.keys())[0]
		else:
			self.visible = visible

	@property
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, value):
		self._visible = value
		self._update_show_hide()

	def _generate_panels(self):
		# make all the sub layouts for the different conditions
		return {
			key: ensure_widget(sub_layout) for key, sub_layout in self.layouts.items()
		}

	def _update_show_hide(self, *_):
		for key, panel in self._conditional_panels.items():
			panel.setVisible(key == self._visible)

