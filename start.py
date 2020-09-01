import os
from core.logger import log
# This shit is showing warnings in VS Code, but it works, so fuck you
while True:
	try:
		os.system('python berry.py')
	except Exception as exc:
		log.exception(exc)
