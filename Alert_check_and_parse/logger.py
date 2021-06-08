import logging
import logging.config
import datetime

"""
Simple wrapper for logging data 
Used to log data 
"""

logging.basicConfig(filename='alert_parser_debugging//'+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.log',encoding='utf-8', level=logging.DEBUG)
logging.debug('Running server logger')
logger = logging.getLogger('red_Alert_logger')
logging.config.dictConfig({'version': 1,'disable_existing_loggers': True})

#add to log file
def add_to_log(x):
    logging.debug(str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+": "+x)
