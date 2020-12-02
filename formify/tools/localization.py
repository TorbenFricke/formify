import json


class Translator:
	def __init__(self, language="en"):
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
			self.__dict__.update(json.load(f))

	def save(self, file_name):
		with open(file_name, "w+") as f:
			json.dump(self.__dict__, f, indent=4, sort_keys=True)


def load_save_translator(*args, **kwargs) -> Translator:
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
	})
	return translator


def simple_language_switch(language_index):
	def translate(*args):
		if len(args) <= language_index:
			return args[0]
		return args[language_index]

	return translate