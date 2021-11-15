from PySide6 import QtWidgets, QtGui

def _make_h(css_label):
	def func(label):
		widget = QtWidgets.QLabel(text=label)
		widget.setWhatsThis(css_label)
		return widget
	return func


h1 = _make_h("h1")
h2 = _make_h("h2")
h3 = _make_h("h3")
h4 = _make_h("h4")
h5 = _make_h("h5")
text = _make_h("text")
mute = _make_h("mute")