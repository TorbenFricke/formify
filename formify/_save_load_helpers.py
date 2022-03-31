import os
import pathlib
import threading
import time


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


def ensure_appdata_dir(app_name: str = None):
	if app_name is None:
		# import here to prevent circular imports
		from formify import app
		app_name = app.name

	if os.getenv('APPDATA') is not None:
		# windows
		path = pathlib.Path(os.getenv('APPDATA'))
	else:
		# macos
		path = pathlib.Path().home()
		path = path / "Library" / "Application Support"

	path /= app_name
	# TODO Linux
	path.mkdir(parents=True, exist_ok=True)
	return path