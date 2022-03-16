from formify.layout import Col
from formify.controls._base import set_props
from PySide6 import QtWidgets, QtCore


class Segment(QtWidgets.QFrame):
	def __init__(self, layout_or_control, *args, margin=7, **kwargs):
		super().__init__()
		self.setContentsMargins(margin, margin, margin, margin)
		set_props(self, kwargs)

		if isinstance(layout_or_control, QtWidgets.QLayout) and len(args) == 0:
			self.setLayout(layout_or_control)
		else:
			self.setLayout(Col(
				layout_or_control,
				*args
			))


class SegmentLight(Segment):
	pass


class SegmentAlt(Segment):
	pass


class SegmentRed(Segment):
	pass


class SegmentYellow(Segment):
	pass


class SegmentGreen(Segment):
	pass


class SegmentBlue(Segment):
	pass


class SegmentPurple(Segment):
	pass


class SegmentSidebar(Segment):
	pass
