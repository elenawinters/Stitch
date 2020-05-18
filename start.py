import os
from core.logger import log
while True:
	try:
		os.system('python berry.tls.py')
	except Exception as exc:
		log.exception(exc)
