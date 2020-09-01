from core.logger import log
import sys
import os
# This shit is showing warnings in VS Code, but it works, so fuck you
while True:
	try:
		os.system(sys.executable + 'berry.py')
	except Exception as exc:
		log.exception(exc)
