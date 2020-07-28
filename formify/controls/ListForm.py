from formify.controls import Form
from formify.layout import Row, ensure_widget
from formify.controls import ControlList
from formify.controls._events import suspend_updates
import typing


class ListForm(Form):
	def __init__(self, model_form: Form, items:typing.List=None, label:str="",*args, **kwargs):
		self.model_form = model_form
		self._suspend_update_events = False

		# generate the master layout containing all widgets and sub layouts
		self.control = ControlList(label=label, items=items, add_click=self.new_item)
		layout = Row(
			self.control,
			self.model_form
		)

		# initialize superclass
		Form.__init__(self, layout=layout, *args, **kwargs)

		# update the form when list selection changes
		self._update_form()
		self.control.index_change.subscribe(self._update_form)

		# update list, when the form changes
		self.model_form.change.subscribe(self._update_list)


	def new_item(self):
		self.control.items += [(self.model_form.value, "New Item")]
		self.control.index = len(self.control.items) - 1


	def _update_form(self, *args):
		if self._suspend_update_events:
			return
		with suspend_updates(self):
			print("_update_form")
			form_data = self.control.selected_item[0]
			if form_data is None:
				return
			self.model_form.value = self.control.selected_item[0]


	def _update_list(self):
		if self._suspend_update_events:
			return
		with suspend_updates(self):
			print("_update_list")
			form_data = self.model_form.value
			self.control.selected_item = (
				form_data,
				str(form_data)
			)