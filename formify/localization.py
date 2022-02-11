import json


class Translator:

	def __init__(self, language: str = None):
		"""
		By the default, the system language is used (i.e. "en", "de", "fr", ...)
		"""
		# get the systems default language
		if language is None:
			import locale
			language = locale.getdefaultlocale()[0].split("_")[0]
		self.language = language
		"""Set the current language (usually a language code)"""
		self.translations = {}

	def add(self, id: str, **langauges):
		"""
		Add translations for an id. You can use any string as `id.

		```
		translator = Translator()
		translator.add("file", en="file", de="Datei"})

		translator.language = "de"
		print(translator("file")) # returns "Datei"
		```
		"""
		self.translations[id] = langauges
		return self(id)

	def __call__(self, id: str):
		"""
		Grab the translation for id based on the current language. Always returns a string.
		If no translation for the current language `translator.language` is provided, the id is returned.

		```
		translator("file_name")
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
	Returns a `Translator`, prepopulated with a few default german english translations.
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
	})
	return translator


def language_switch(translator: Translator, language_order: list) -> callable:
	def switch(*args):
		try:
			index = language_order.index(translator.language)
		except:
			index = 0
		return args[index]

	return switch