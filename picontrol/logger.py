#!/usr/bin/env
# logger.py

import logging
import os
import tempfile
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from rich.logging import RichHandler


def create_logger(name: str = 'picontrol') -> logging.Logger:
    """
    Create a logger for easier debugging

    :param name: name of the logger
    :return: logger object
    :rtype: logging.Logger
    """
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    today = datetime.now().strftime("%Y%m%d")
    rich_handler = RichHandler(rich_tracebacks=False, markup=True)
    file_handler = TimedRotatingFileHandler(
        filename=f"{tempfile.gettempdir()}{os.sep}{name}_{today}.log",
        when="D",
        interval=3,
        backupCount=10,
    )

    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        datefmt="[%Y/%m/%d %H:%M;%S]",
        handlers=[rich_handler, file_handler],
    )
    logger = logging.getLogger("rich")
    return logger
