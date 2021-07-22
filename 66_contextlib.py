import logging
import contextlib

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything

@contextlib.contextmanager
def log_level(level, name):
	logger = logging.getLogger(name)
	old_level = logger.getEffectiveLevel()
	logger.setLevel(level)
	try:
		yield logger
	finally:
		logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my-log') as logger:
	logger.debug(f'This is a message for {logger.name}!')
	logging.debug('This will not print')