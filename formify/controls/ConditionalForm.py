from formify.controls import Form
from formify.layout import Col, ensure_widget
from formify.controls import ControlCombo


def _make_condition_control(layouts):
	return ControlCombo(
		variable_name="type",
		label="Type",
		items=[(key, key) for key in layouts.keys()]
	)


class ConditionalForm(Form):
	def __init__(self, layouts:dict, condition_control=None, *args, **kwargs):
		self.layouts = layouts

		# make conditional control
		if condition_control is None:
			self.condition_control = _make_condition_control(layouts)
		else:
			self.condition_control = condition_control

		self._conditional_panels = {}

		# generate the master layout containing all widgets and sub layouts
		layout = self._generate()

		# initialize superclass
		Form.__init__(self, layout=layout, *args, **kwargs)

		# only show relevant the form
		self._update_show_hide()
		self.change.subscribe(self._update_show_hide)


	def _generate(self):
		# make all the sub layouts for the different conditions
		for key, sub_layout in self.layouts.items():
			self._conditional_panels[key] = ensure_widget(sub_layout)

		# the global layout, everything gets put into
		master_layout = Col(
			self.condition_control,
			*list(self._conditional_panels.values()),
		)

		return master_layout


	def _update_show_hide(self, *_):
		condition = self.condition_control.value
		for key, panel in self._conditional_panels.items():
			panel.setVisible(key == condition)

