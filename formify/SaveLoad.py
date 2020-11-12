import json, warnings, threading, time, pathlib, os
from formify.controls import Form
from formify.tools import save_dialog, open_dialog, yes_no_dialog, ok_dialog
from formify.controls._events import EventDispatcher


def default_save(form, file_name):
	with open(file_name, "w+") as f:
		f.write(
			json.dumps(form.all_values, indent=4)
		)


def default_open(form, file_name):
	with open(file_name) as f:
		s = f.read()
	form.all_values = json.loads(s)


class Timer(threading.Thread):
	def __init__(self, interval, target):
		threading.Thread.__init__(self)
		self.daemon = True
		self.interval = interval
		self.target = target
		self.start()

	def run(self):
		while True:
			time.sleep(self.interval)
			self.target()


def ensure_appdata_dir():
	# import here to prevent circular imports
	from formify import app
	path = pathlib.Path(os.getenv('APPDATA')) / app.name
	path.mkdir(parents=True, exist_ok=True)
	return path


class LoadSaveHandler:
	def __init__(self,
	             main_form: Form,
	             allowed_file_extensions:list=None,
	             save_handler=default_save,
	             open_handler=default_open):

		self.form = main_form
		self.allowed_file_extensions = allowed_file_extensions

		self.save_handler = save_handler
		self.open_handler = open_handler

		# file name
		self._file_name = ""
		self.file_name_changed = EventDispatcher(self)

		# keep track of number of changes
		self._no_changes = 0
		def inc_changes():
			self.no_changes += 1
			self.no_autosave_changes += 1
		self.form.change.subscribe(inc_changes)
		self.no_changes_changed = EventDispatcher(self)

		# restore
		self.autosave_filename = ensure_appdata_dir() / "autosave.json"
		if self.restore():
			ok_dialog("Data Restored", "Data was restored from autosave")

		# start autosave timer
		self.autosave_timer = Timer(5, self.autosave)
		self.no_autosave_changes = 0


	@property
	def file_name(self):
		return self._file_name


	@file_name.setter
	def file_name(self, value):
		self._file_name = value
		self.file_name_changed(value)


	@property
	def no_changes(self):
		return self._no_changes


	@no_changes.setter
	def no_changes(self, value):
		self._no_changes = value
		self.no_changes_changed(value)


	def menu(self):
		return {
			"Open...": (self.open, "ctrl+o"),
			"Save": (self.save, "ctrl+s"),
			"Save as...": (self.save_as, "ctrl+shift+s")
		}


	def file_extension_filter(self):
		if self.allowed_file_extensions is not None:
			return ";;".join([f"*.{ext}" for ext in self.allowed_file_extensions])
		else:
			return "*"


	def save(self):
		if self.file_name == "":
			self.save_as()
			return
		self.save_handler(self.form, self.file_name)
		self.no_autosave_changes = 0
		self.no_changes = 0


	def save_as(self):
		self.file_name = save_dialog(title="Save as...", filter=self.file_extension_filter())
		if self.file_name == "":
			return
		self.save()


	def open(self):
		if self.no_changes > 0 and not yes_no_dialog(
				"Are you sure?",
				"All current changes will be lost. Are you sure you want to open another file?"):
			return
		self.file_name = open_dialog(title="Open...", filter=self.file_extension_filter())
		if self.file_name == "":
			return
		self.open_handler(self.form, self.file_name)
		self.no_changes = 0


	def autosave(self):
		if self.no_autosave_changes > 0:
			try:
				default_save(self.form, self.autosave_filename)
				self.no_autosave_changes = 0
			except:
				pass


	def purge_autosave(self):
		os.remove(self.autosave_filename)


	def restore(self):
		if not os.path.exists(self.autosave_filename):
			return False
		try:
			default_open(self.form, self.autosave_filename)
		except:
			return False
		else:
			return True