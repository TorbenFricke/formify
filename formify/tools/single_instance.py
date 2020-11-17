import sys, os, tempfile

class SingleInstance:
	"""
	Stolen from:
	https://pythonhosted.org/tendo/_modules/tendo/singleton.html
	"""

	def __init__(self, already_running_callback:callable=None):
		self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' +
		    os.path.splitext(os.path.abspath(__file__))[0].replace("/","-").replace(":","").replace("\\","-")  + '.lock')
		if sys.platform == 'win32':
			try:
				# file already exists, we try to remove (in case previous execution was interrupted)
				if os.path.exists(self.lockfile):
					os.unlink(self.lockfile)
				self.fd =  os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
			except OSError as e:
				if e.errno == 13:
					if already_running_callback is not None:
						already_running_callback()
					sys.exit(-1)
				print(e.errno)
				raise
		else: # non Windows
			import fcntl
			self.fp = open(self.lockfile, 'w')
			try:
				fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				sys.exit(-1)

	def __del__(self):
		if sys.platform == 'win32':
			if hasattr(self, 'fd'):
				os.close(self.fd)
				os.unlink(self.lockfile)