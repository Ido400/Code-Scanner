import logging
from functools import wraps
from logging.handlers import TimedRotatingFileHandler

def create_logger(logger_name:str):
	#create a logger object
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.INFO)
	logFormat = "%(asctime)s %(levelname)-8s --- [%(name)-8s] : %(message)s"
	logFormatter = logging.Formatter(logFormat)
	logging.basicConfig(filename=f"./logs/{logger_name}.log", format=logFormat,	level=logging.INFO)
	fileHandler = TimedRotatingFileHandler(
            f"./logs/{logger_name}.log", when="midnight")
	#create a file to store all the
	# logged exceptions
	fileHandler.setFormatter(logFormatter)
	fileHandler.suffix = "%Y_%m_%d"
	logger.addHandler(fileHandler)

	return logger


def exception(logger):
	
	# logger is the logging object
	# exception is the decorator objects
	# that logs every exception into log file
	def decorator(func):
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			
			try:
				return func(*args, **kwargs)
			
			except:
				issue = "exception in "+func.__name__+"\n"
				issue = issue+"-------------------------\
				------------------------------------------------\n"
				logger.exception(issue)
				raise
		return wrapper
	return decorator


