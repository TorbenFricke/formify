import json


class Translator:
	def __init__(self, language:str=None):
		# get the systems default language
		if language is None:
			import locale
			language = locale.getdefaultlocale()[0].split("_")[0]
		self.language = language
		self.translations = {}

	def add(self, id, **langauges):
		self.translations[id] = langauges
		return self(id)

	def __call__(self, id):
		# grab the specified id, or an empty dict
		translations = self.translations.get(id, {})
		# return id, if the language was not found
		return translations.get(self.language, id)

	def load(self, file_name):
		with open(file_name) as f:
			self.translations.update(json.load(f))

	def save(self, file_name):
		with open(file_name, "w+") as f:
			json.dump(self.translations, f, indent=2, sort_keys=True)


def default_translator(*args, **kwargs) -> Translator:
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