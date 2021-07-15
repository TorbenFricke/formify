from PySide6 import QtWidgets


def extract_file_name(dialog_return: tuple):
	file_name = dialog_return[0].url()
	# clean file name
	if file_name[:7] == "file://":
		file_name = file_name[7:]

	# strip slashes on windows
	import os
	if os.name == "nt":
		file_name = file_name.strip("/")
	return file_name


def save_dialog(title="Save as...", **kwargs):
	return extract_file_name(
		QtWidgets.QFileDialog().getSaveFileUrl(
			caption=title,
			**kwargs,
		)
	)

def open_dialog(path=None, title="Open...", **kwargs):
	return extract_file_name(
		QtWidgets.QFileDialog().getOpenFileUrl(
			caption=title,
			**kwargs
		)
	)