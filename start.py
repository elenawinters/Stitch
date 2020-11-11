from core.logger import log, trace
import sys
import os

title = '| Stitch'

if __name__ == '__main__':
	log.debug(sys.version)

	print(f"\033]0;{title}\007", flush='', end='')  # This works on Windows, and is also claimed to work on other platforms

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	while True:
		try:
			print(trace.reset, end='')  # Fix color
			os.system(sys.executable + ' berry.py')
		except Exception as exc:
			log.exception(exc)
