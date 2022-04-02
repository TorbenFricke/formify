import json
import locale


class Translator:
	"""
	By the default, the system language is used (i.e. "en", "de", "fr", ...)
	"""
	def __init__(self, language: str = None):
		# get the systems default language
		if language is None:
			language = locale.getdefaultlocale()[0].split("_")[0]
		self.language = language
		"""Set the current language (usually a language code)"""
		self.translations = {}

	def add(self, id: str, **langauges):
		"""
		Add translations for an id. You can use any string as `id.

		```
		translator = Translator()
		translator.add("button_open", en="Open", de="Öffnen"})

		translator.language = "de"
		print(translator("button_open")) # returns "Öffnen"
		```
		"""
		self.translations[id] = langauges
		return self(id)

	def __call__(self, id: str):
		"""
		Grab the translation for id based on the current language. Always returns a string.
		If no translation for the current language `translator.language` is provided, the id is returned.

		```
		translator("button_open")
		```
		"""
		# grab the specified id, or an empty dict
		translations = self.translations.get(id, {})
		# return id, if the language was not found
		return translations.get(self.language, id)

	def load(self, file_name: str):
		"""
		Reads all translations into a JSON file.
		"""
		with open(file_name) as f:
			self.translations.update(json.load(f))

	def save(self, file_name: str):
		"""
		Dumps all translations into a JSON file.
		"""
		with open(file_name, "w+") as f:
			json.dump(self.translations, f, indent=2, sort_keys=True)


def default_translator(*args, **kwargs) -> Translator:
	"""
	Returns a `Translator`, populated with translations for default menu items (Open, Close, ...) for german and english.
	*args and **kwargs are passed to the Translator(*args, **kwargs).
	"""
	translator = Translator(*args, **kwargs)
	translator.translations.update({
		"Open...": {"de": "Öffnen..."},
		"Open Recent": {"de": "Zuletzt Geöffnet"},
		"Save": {"de": "Speichern"},
		"Save As...": {"de": "Speichern Unter..."},
		"Are you sure?": {"de": "Sind Sie sich sicher?"},
		"All current changes will be lost. Are you sure you want to open another file?": {
			"de": "Alle Änderungen werden verworfen. Möchten Sie wirklich eine andere Datei öffnen?"},
		"File not found": {"de": "Die Datei wurde nicht gefunden"},
		"does not seem to exist.": {"de": "scheint nicht zu existieren."},
		"restored": {"de": "wiederhergestellt"},
		"File": {"de": "Datei"},
		"+ Add": {"de": "+ Hinzufügen"},
		"- Remove": {"de": "- Löschen"},
		"Undo": {"de": "Rückgängig Machen"},
		"Redo": {"de": "Wiederholen"},
		"Cut": {"de": "Ausschneiden"},
		"Copy": {"de": "Kopieren"},
		"Paste": {"de": "Einfügen"},
		"Delete": {"de": "Löschen"},
		"Select All": {"de": "Alles Auswählen"},
	})
	return translator


def make_language_switch(translator: Translator, language_order: list) -> callable:
	"""
	Makes a function, that selects the argument corresponding to the current language. Best read the example below:

	```
	translator = Translator()
	switch = make_language_switch(translator, ["en", "de"])

	translator.language = "en"
	print(switch("open", "öffnen")) # prints "open"

	translator.language = "de"
	print(switch("open", "öffnen")) # prints "öffnen"

	# set the text of a button
	ControlButton(switch("open", "öffnen"))
	```

	Args:
		translator: used to determine the current language
		language_order: language order of the language switch arguments

	Returns:

	"""
	def switch(*args):
		try:
			index = language_order.index(translator.language)
		except:
			index = 0
		return args[index]

	return switch