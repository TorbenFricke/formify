from PySide2 import QtWidgets


def extract_file_name(dialog_return: tuple):
	file_name = dialog_return[0].url()
	# clean file name
	if file_name[:7] == "file://":
		file_name = file_name[7:]
	return file_name


def save_dialog(title="Save as..."):
	return extract_file_name(
		QtWidgets.QFileDialog().getSaveFileUrl(
			caption=title,
		)
	)

def open_dialog(path=None, title="Open..."):
	return extract_file_name(
		QtWidgets.QFileDialog().getOpenFileUrl(
			caption=title,
		)
	)