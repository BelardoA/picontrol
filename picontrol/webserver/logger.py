#!/usr/bin/env python
# logger.py

import logging
import os
import tempfile
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class CustomHandler(logging.StreamHandler):
    """
    A simple logging handler that formats log messages.
    """

    def format(self, record):
        formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s",
                                     "[%Y/%m/%d %H:%M:%S]")
        return formatter.format(record)


def create_logger(name='picontrol'):
    """
    Create a logger for easier debugging

    :param str name: name of the logger, defaults to picontrol
    :return: logger object
    :rtype: logging.Logger
    """
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    today = datetime.now().strftime("%Y%m%d")
    custom_handler = CustomHandler()
    file_handler = TimedRotatingFileHandler(
        filename=tempfile.gettempdir() + os.sep + name + "_" + today + ".log",
        when="D",
        interval=3,
        backupCount=10,
    )

    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        datefmt="[%Y/%m/%d %H:%M:%S]",
        handlers=[custom_handler, file_handler],
    )
    logger = logging.getLogger(name)
    return logger
