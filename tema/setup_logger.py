"""
Setup logger for the application.
"""

import logging
from logging.handlers import RotatingFileHandler
import time


logger = logging.getLogger("marketplace_logger")
logger.propagate = False

logging.basicConfig(filename="marketplace.log", level=logging.INFO)

RFH_LOGGER = RotatingFileHandler('marketplace.log', backupCount=5)
RFH_LOGGER.setLevel(logging.INFO)

RFH_FORMATTER = logging.Formatter(
    '%(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
RFH_FORMATTER.converter = time.gmtime

RFH_LOGGER.setFormatter(RFH_FORMATTER)

logger.addHandler(RFH_LOGGER)
