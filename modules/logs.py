import logging.handlers
import logging, os
import modules.configuration as configuration

logger = logging.getLogger()

def start():
    configuration.load()
    debug = configuration.get_value("General", "debug") or False
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create a TimedRotatingFileHandler to create a new log file every day
    handler = logging.handlers.TimedRotatingFileHandler(
        filename="logs/rfp.log", 
        when="w0",  # Rotate at midnight
        backupCount=31    # Keep the last 31 log files
    )
    
    # Set the logging format and level on the handler
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)

    if debug:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
