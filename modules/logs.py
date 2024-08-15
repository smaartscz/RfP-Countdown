import logging.handlers
import logging, os

logger = logging.getLogger()

def start():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create a TimedRotatingFileHandler to create a new log file every day
    handler = logging.handlers.TimedRotatingFileHandler(
        filename="logs/rfp.log", 
        when="midnight",  # Rotate at midnight
        interval=1,       # Rotate every day
        backupCount=31    # Keep the last 31 log files
    )
    
    # Set the logging format and level on the handler
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
