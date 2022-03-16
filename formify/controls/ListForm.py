from formify.controls import Form
from formify.layout import SplitterRow
from formify.controls import ControlList, _item_base
import typing


class ListForm(Form):
	def __init__(
			self,
			model_form: Form,
			value: typing.List = None,
			label: str = "",
			display_name_callback: typing.Callable = str,
			list_control: _item_base.ListBase = None,
			layout_class=SplitterRow,
			on_change=None,
			**kwargs
	):
		self.model_form = model_form

		# generate the master layout containing all widgets and sub layouts
		if list_control is None:
			self.control = ControlList(label=label)
		else:
			self.control = list_control
		self.control.add_click = self.new_item

		layout = layout_class(
			self.control,
			self.model_form
		)

		self.control.display_name_callback = display_name_callback

		# initialize superclass
		Form.__init__(self, layout=layout, **kwargs)

		# update the form when list selection changes
		self._suspend_update_form = False
		self._update_form()
		self.control.index_change.subscribe(self._update_form)
		self.control.items_change.subscribe(self._update_form)

		# set own event handler to the event handler of the child ControlList.
		# Its important to bring the subscriptions with it
		self.change = self.control.items_change
		if on_change is not None:
			self.change.subscribe(on_change)

		# update list, when the form changes
		self.model_form.change.subscribe(self._update_list)

		# set initial rows
		if value is not None:
			self.value = value

	def new_item(self):
		self.control.items += [self.model_form.value]
		self.control.index = len(self.control.items) - 1

	def _update_form(self, *_):
		if self._suspend_update_form:
			return

		if self.control.index == -1:
			# nothing is selected? hide the Form and return early.
			self.model_form.setEnabled(False)
			return
		else:
			self.model_form.setEnabled(True)

		with self.model_form.change.suspend_updates():
			#print("_update_form")
			form_data = self.control.selected_item
			if form_data is None:
				return
			self.model_form.value = self.control.selected_item

		self.repaint()

	def _update_list(self):
		try:
			self._suspend_update_form = True
			with self.control.index_change.suspend_updates():
				#print("_update_list")
				if self.control.items is None or len(self.control.items) == 0:
					return
				form_data = self.model_form.value
				self.control.selected_item = form_data
		finally:
			self._suspend_update_form = False

	def get_value(self):
		return self.control.items

	def set_value(self, value):
		self.control.items = value

	def get_all_values(self):
		return self.value

	def set_all_values(self, value):
		self.value = value
