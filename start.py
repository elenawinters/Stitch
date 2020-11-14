from core.logger import log, trace
import threading
import asyncio
import berry
import sys
import os

title = '| Stitch'


def start():
	log.debug(sys.version)

	print(f"\033]0;{title}\007", flush='', end='')  # This works on Windows, and is also claimed to work on other platforms

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	while True:
		try:
			t = threading.Thread(target=berry.start, name='Stitch', daemon=True)
			t.start()
			t.join()
		except Exception as exc:
			log.exception(exc)


if __name__ == '__main__':
	start()
