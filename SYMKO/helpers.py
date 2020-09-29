from formify.controls import *

class ControlTextList(ControlText):
	def __init__(self, *args, **kwargs):
		super(ControlTextList, self).__init__(*args, **kwargs)

	@property
	def value(self):
		return [ControlText.value.fget(self)]

	@value.setter
	def value(self, value):
		ControlText.value.fset(self, value[0])


class ControlComboList(ControlCombo):
	def __init__(self, *args, **kwargs):
		super(ControlComboList, self).__init__(*args, **kwargs)

	@property
	def value(self):
		return [ControlCombo.value.fget(self)]

	@value.setter
	def value(self, value):
		ControlCombo.value.fset(self, value[0])


class ControlFileList(ControlFile):
	def __init__(self, *args, **kwargs):
		super(ControlFileList, self).__init__(*args, **kwargs)

	@property
	def value(self):
		return [ControlFile.value.fget(self)]

	@value.setter
	def value(self, value):
		ControlFile.value.fset(self, value[0])