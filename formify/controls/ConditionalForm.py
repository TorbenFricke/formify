from formify.controls import Form
from formify.controls.Form import walk, extract_values_dict
from formify.layout import Col, ensure_widget
from formify.controls import ControlSelect


def _make_condition_control(layouts):
	return ControlSelect(
		variable_name="type",
		label="Type",
		items=[key for key in layouts.keys()]
	)


class ConditionalForm(Form):
	def __init__(self, layouts: dict, condition_control=None, *args, **kwargs):
		self.layouts = layouts

		# make conditional control
		if condition_control is None:
			self.condition_control = _make_condition_control(layouts)
		else:
			self.condition_control = condition_control

		self._conditional_panels = {}
		self._controls_by_condition = {}

		# generate the master layout containing all widgets and sub layouts
		layout = self._generate()

		# initialize superclass
		Form.__init__(self, layout=layout, *args, **kwargs)

		# only show relevant the form
		self._update_show_hide()
		self.change.subscribe(self._update_show_hide)
		if not self._update_show_hide in self.condition_control.change.subscriptions:
			self.condition_control.change.subscribe(self._update_show_hide)


	def _generate(self):
		# make all the sub layouts for the different conditions
		for key, sub_layout in self.layouts.items():
			self._conditional_panels[key] = ensure_widget(sub_layout)
			self._controls_by_condition[key] = walk(self._conditional_panels[key])

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

	def get_value(self):
		out = extract_values_dict(self._controls_by_condition[self.condition_control.value])
		out[self.condition_control.variable_name] = self.condition_control.value
		return out

	def get_all_values(self):
		# We want to do this complicated dance instead of just writing "retrun extract_values_dict(self.controls)" to
		# make sure, the values of the currently shown controls 'win' if there are multiple controls with the same
		# variable_name.
		out = {}
		conditional = self.condition_control.value
		for key, controls in self._controls_by_condition.items():
			if key == conditional:
				continue
			out.update(extract_values_dict(controls, all_values=True))
		out.update(extract_values_dict(self._controls_by_condition[conditional], all_values=True))
		out[self.condition_control.variable_name] = self.condition_control.value
		return out