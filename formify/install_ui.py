from formify import *
import os, subprocess


def _file_and_image_ui(name, valriable_prefix, more_ui=None):
	control_file = ControlFile("", variable_name=f"{valriable_prefix}_file")
	control_image = ControlImage()
	check_enabled = ControlCheckbox(
		f"Set a custom {name.lower()} for the application",
		variable_name=f"{valriable_prefix}",
		value=False
	)

	error_text = h5("")
	error_segment = SegmentRed(error_text)
	error_segment.hide()

	def update_image():
		if not check_enabled.value:
			error_segment.hide()
			control_image.setEnabled(False)
			control_file.setEnabled(False)
		else:
			control_image.setEnabled(True)
			control_file.setEnabled(True)

		file_name = control_file.value

		if not os.path.isfile(file_name):
			error_text.setText(
				f"Cannot load image file <b>{file_name}</b>"
			)
			error_segment.show()
		else:
			error_segment.hide()

		control_image.file_name = file_name

	control_file.change.subscribe(update_image)
	check_enabled.change.subscribe(update_image)

	return Col(
		h2(name),
		check_enabled,
		more_ui,
		control_file,
		error_segment,
		control_image,
	)


def main():
	app.name = "formify-install"

	command = ControlTextarea("Command", variable_name="cmd")
	command.read_only = True

	excludes = [
		"matplotlib",
		"numpy",
		"PySide6.QtWebEngineWidgets",
	]
	excludes_default = [
		"PySide6.QtQml",
		"PySide6.QtQuickWidgets",
		"PySide6.QtPrintSupport",
		"PySide6.QtQuick",
		"PySide6.Quick",
		"PySide6.Qml",
		"PySide6.QtNetwork",
	]

	ui_excludes = Form(Col(
		h2("Exclude Modules"),
		SegmentBlue(text("Excluding unnecessary modules saves disk space and startup time")),
		Grid(
			*[ControlCheckbox(variable_name=name, value=False) for name in excludes],
			*[ControlCheckbox(variable_name=name, value=True) for name in excludes_default],
		),
		ControlTextarea("Other Excluded Modules (seperated by newline)", variable_name="_others"),
	), variable_name="excludes")

	ui_general = Col(
		h2("General Settings"),
		SegmentYellow(
			ControlCheckbox("Create a one-file bundled executable", variable_name="onefile", value=False),
			text("A one-file bundled executable can significantly slow down initial startup.")
		),
		ControlCheckbox("Replace files in output directory without asking", variable_name="noconfirm", value=True),
		ControlCheckbox("Clean flies from previous build", variable_name="clean", value=True),
		ControlFile("Output directory (Leave empty for default './dist')", variable_name="dist"),
		ControlFile("Temporary working directory (Leave empty for default './build')", variable_name="build"),
	)

	entry = ControlFile("Entry point (initial script)", variable_name="entry")
	entry_error = SegmentRed(text("No valid entry point. Please select a Python script."))

	def update_entry_error():
		entry_error.setVisible(not os.path.isfile(entry.value))

	entry.change.subscribe(update_entry_error)

	progress = ControlProgress()
	progress.spin()
	progress.setVisible(False)

	@tools.BackgroundMethod
	def install():
		#tools.do_in_ui_thread(lambda: progress.setVisible(True))

		# Needs to be shell since start isn't an executable, its a shell cmd
		os.system(f"start /wait cmd  /k {command.value}")

		#tools.do_in_ui_thread(lambda: progress.setVisible(False))

	os_warning = None
	if not os.name == "nt":
		os_warning = SegmentRed(
			h3("formify-install does not support this OS"),
			text("The formify-installer only really works on windows. Directly use 'pyinstaller' on other platforms."),
		)

	ui = Form(SplitterCol(
		Col(
			os_warning,
			entry,
			entry_error,
			Tabs({
				"General": 	ui_general,
				"Exlcude Modules": 	ui_excludes,
				"Icon": _file_and_image_ui("Icon", "icon", SegmentBlue(
					text(".ico and .exe are allowed file endings. Thre preview does not work for exe files.")
				)),
				"Splash Screen": _file_and_image_ui("Splash Screen", "splash", SegmentBlue(
					text(".png and .jpg are allowed file endings. "
					   "Do not use 'formify.show_spashscreen()' if you use this option. "
					   "Otherwise you will get two spashscreens.")
				)),
			}),
		),
		Col(
			command,
			Row(
				ControlButton("Bundle Executable", on_click=install),
				progress,
			),
		)
	))

	def update_command():
		d = ui.value

		cmd = 'pyinstaller "{}" --noconsole --collect-data formify'.format(d['entry'])
		if d['noconfirm']:
			cmd += " --noconfirm"
		if d['onefile']:
			cmd += " --onefile"
		if d['clean']:
			cmd += " --clean"
		if d['dist']:
			cmd += ' --distpath "{}"'.format(d['dist'])
		if d['build']:
			cmd += ' --workpath "{}"'.format(d['build'])

		for module, exclude in d["excludes"].items():
			if exclude and module != "_others":
				cmd += ' --exclude-module "{}"'.format(module)
		for line in d["excludes"]["_others"]:
			cmd += ' --exclude-module "{}"'.format(line.strip())

		if d["icon"]:
			cmd += ' --icon "{}"'.format(d["icon_file"])
		if d["splash"]:
			cmd += ' --splash "{}"'.format(d["splash_file"])

		command.value = cmd

	ui.change.subscribe(update_command)


	MainWindow(
		ui,
		title="Formify Installer",
		margin=8,
	)


if __name__ == "__main__":
	main()
