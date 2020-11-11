from formify.controls import ControlMessagebox


def yes_no_dialog(title="Sure?", text="Are you sure?"):
	return ControlMessagebox(title, text).show()


def yes_no_abort_dialog(title="Sure?", text="Are you sure?"):
	class YesNoAbort(ControlMessagebox):
		def make_buttons(self):
			self.setStandardButtons(self.Yes)
			self.addButton(self.No)
			self.addButton(self.Abort)
			self.setDefaultButton(self.Abort)

	return YesNoAbort(title, text).show()


def ok_dialog(title="Information", text="Something is going to happen!"):
	class Ok(ControlMessagebox):
		def make_buttons(self):
			self.setStandardButtons(self.Ok)
			self.setDefaultButton(self.Ok)

	return Ok(title, text).show(ControlMessagebox.Ok)