
import logging
from functools import wraps

def create_logger(logger_name:str):
	import logging
	#create a logger object
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.INFO)
	
	logging.basicConfig(filename=f"./logs/{logger_name}.log")
	#create a file to store all the
	# logged exceptions
	logfile = logging.FileHandler(f"./logs/{logger_name}.log")
	
	fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	formatter = logging.Formatter(fmt)
	
	logfile.setFormatter(formatter)
	logger.addHandler(logfile)
	
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
		
		return wrapper
	return decorator


