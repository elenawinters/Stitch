from core.logger import log
import sys
import os

# Restart loop, so if program stops, it restarts
if __name__ == '__main__':
	while True:
		try:
			os.system(sys.executable + ' berry.py')
		except Exception as exc:
			log.exception(exc)
