import logging
from logging.handlers import RotatingFileHandler
import time


logger = logging.getLogger("marketplace_logger")
logger.propagate = False

logging.basicConfig(filename="marketplace.log", level=logging.INFO)

rfh_logger = RotatingFileHandler('marketplace.log', backupCount=5)
rfh_logger.setLevel(logging.INFO)

rfh_formatter = logging.Formatter(
    '%(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
rfh_formatter.converter = time.gmtime

rfh_logger.setFormatter(rfh_formatter)

logger.addHandler(rfh_logger)
