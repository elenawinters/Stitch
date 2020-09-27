from core.logger import log
import ctypes
import sys
import os

# Restart loop, so if program stops, it restarts
if __name__ == '__main__':
	if sys.platform == "win32":
		ctypes.windll.kernel32.SetConsoleTitleW("Stitch")
	elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
		print("\033]0;Stitch\007", flush='')

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	while True:
		try:
			os.system(sys.executable + ' berry.py')
		except Exception as exc:
			log.exception(exc)
