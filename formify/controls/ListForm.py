from formify.controls import Form
from formify.layout import SplitterRow
from formify.controls import ControlList
from formify.controls._events import suspend_updates
import typing


class ListForm(Form):
	def __init__(self, model_form: Form, value:typing.List=None, label:str="",
	             display_name_callback:typing.Callable=str, *args, **kwargs):
		self.model_form = model_form
		self._suspend_update_events = False
		self.repr = display_name_callback

		# generate the master layout containing all widgets and sub layouts
		self.control = ControlList(label=label, add_click=self.new_item)
		layout = SplitterRow(
			self.control,
			self.model_form
		)

		# initialize superclass
		Form.__init__(self, layout=layout, *args, **kwargs)

		# update the form when list selection changes
		self._update_form()
		self.control.index_change.subscribe(self._update_form)

		# set own event handler to the event handler of the child ControlList.
		# Its important to bring the subscriptions with it
		self.control.change.subscriptions += self.change.subscriptions
		self.change = self.control.change

		# update list, when the form changes
		self.model_form.change.subscribe(self._update_list)

		# set initial rows
		if value is not None:
			self.value = value


	def new_item(self):
		value = self.model_form.value
		self.control.items += [(value, self._repr(value))]
		self.control.index = len(self.control.items) - 1


	def _update_form(self, *args):
		if self._suspend_update_events:
			return

		if self.control.index == -1:
			# nothing is selected? hide the Form and return early.
			self.model_form.setVisible(False)
			return
		else:
			self.model_form.setVisible(True)

		with self.model_form.change.suspend_updates():
			#print("_update_form")
			form_data = self.control.selected_item[0]
			if form_data is None:
				return
			self.model_form.value = self.control.selected_item[0]

		self.repaint()

	def _repr(self, x):
		try:
			out = self.repr(x)
		except Exception as e:
			out = str(x)
			print(f"Error while generating string representation "
			      f"for ListForm {self.variable_name}: \n{e}")
		return out


	def _update_list(self):
		if self._suspend_update_events:
			return
		with suspend_updates(self):
			#print("_update_list")
			form_data = self.model_form.value
			self.control.selected_item = (
				form_data,
				self._repr(form_data)
			)

	@property
	def value(self):
		return [value for value, _ in self.control.items]

	@value.setter
	def value(self, value):
		self.control.items = [(val, self._repr(val)) for val in value]

	@property
	def all_values(self):
		return self.value

	@all_values.setter
	def all_values(self, value):
		self.value = value
