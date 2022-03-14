import json, time, os, traceback

from formify._save_load_helpers import Timer, ensure_appdata_dir
from formify.controls import Form
from formify.tools import save_dialog, open_dialog, yes_no_dialog, ok_dialog
from formify.controls._events import EventDispatcher
from formify import app


def default_save(form, file_name):
	with open(file_name, "w+") as f:
		f.write(
			json.dumps(form.all_values)
		)


def default_open(form, file_name):
	try:
		with open(file_name) as f:
			s = f.read()
	except FileNotFoundError:
		return

	form.all_values = json.loads(s)


class LoadSaveHandler:
	def __init__(
			self,
			main_form: Form,
			allowed_file_extensions: list = None,
			save_handler=default_save,
			open_handler=default_open
	):

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
		self.no_autosave_changes = 0
		self.restored_label = ""
		self.autosave_filename = ensure_appdata_dir() / "autosave.json"
		self.restore()

		# start autosave timer
		self.autosave_timer = Timer(5, self.autosave)

		# recently used
		self.recent_filename = ensure_appdata_dir() / "recent.txt"
		self.file_name_changed.subscribe(self.append_recently_used_list)

	@property
	def file_name(self):
		return self._file_name

	@file_name.setter
	def file_name(self, value):
		self._file_name = value
		# opened or saved to a preopper file, remove restored label
		if value != "":
			self.restored_label = ""
		self.file_name_changed(value)

	@property
	def no_changes(self):
		return self._no_changes

	@no_changes.setter
	def no_changes(self, value):
		self._no_changes = value
		self.no_changes_changed(value)

	def menu(self):
		lines = self.read_recently_used_files()

		def make_open_handler(filename):
			return lambda: self.open(filename)

		t = app.translator

		return {
			t("Open..."): (self.open, "ctrl+o"),
			t("Open Recent"): {
				line: make_open_handler(line) for line in lines
			},
			t("Save"): (self.save, "ctrl+s"),
			t("Save As..."): (self.save_as, "ctrl+shift+s")
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
		try:
			self.save_handler(self.form, self.file_name)
		except:
			traceback.print_exc()
		else:
			self.purge_autosave()
			self.no_changes = 0

	def save_as(self):
		self.file_name = save_dialog(title=app.translator("Save As..."), filter=self.file_extension_filter())
		if self.file_name == "":
			return
		self.save()

	def open(self, filename=None):
		t = app.translator

		if self.no_changes > 0 and not yes_no_dialog(
				t("Are you sure?"),
				t("All current changes will be lost. Are you sure you want to open another file?")):
			return

		if not filename:
			self.file_name = open_dialog(title=t("Open..."), filter=self.file_extension_filter())
		else:
			self.file_name = filename

		if self.file_name == "":
			return

		if not os.path.isfile(self.file_name):
			ok_dialog(t("File not found"), f"'{self.file_name}' {t('does not seem to exist.')}")
			return

		try:
			self.open_handler(self.form, self.file_name)
		except:
			traceback.print_exc()
		else:
			self.no_changes = 0
			self.purge_autosave()

	def autosave(self):
		if self.no_autosave_changes > 0:
			try:
				default_save(self.form, self.autosave_filename)
				self.no_autosave_changes = 0
			except:
				pass

	def purge_autosave(self):
		self.no_autosave_changes = 0
		try:
			os.remove(self.autosave_filename)
		except FileNotFoundError:
			pass

	def restore(self):
		if not os.path.exists(self.autosave_filename):
			return False

		try:
			default_open(self.form, self.autosave_filename)
		except json.decoder.JSONDecodeError:
			os.rename(self.autosave_filename, f"{self.autosave_filename}-broken-{time.time()}")
			return False
		except Exception as e:
			traceback.print_exc()

		self.no_autosave_changes = 0
		self.restored_label = f" ({app.translator('restored')})"
		# trigger event to update titlebar
		self.file_name_changed(self.file_name)
		return True

	def append_recently_used_list(self):
		if self.file_name == "":
			return
		with open(self.recent_filename, "a+") as f:
			f.write(self.file_name + "\n")

	def read_recently_used_files(self, n=10):
		if not os.path.isfile(self.recent_filename):
			return []
		try:
			with open(self.recent_filename) as f:
				lines = f.readlines()
		except FileNotFoundError:
			return

		line_iterator = (clean for line in reversed(lines) if (clean := line.strip(" \n")) != "")

		# remove duplicates and reverse
		return remove_duplicates_from_list(line_iterator, max_length=n)


def remove_duplicates_from_list(some_iter, max_length=None):
	if max_length is None:
		max_length = 100000000

	hashes = set()
	de_duplicated = []
	for item in some_iter:
		item_hash = hash(item)
		if item_hash in hashes:
			continue
		hashes.add(item_hash)

		de_duplicated.append(item)

		if len(de_duplicated) == max_length:
			break

	return de_duplicated
