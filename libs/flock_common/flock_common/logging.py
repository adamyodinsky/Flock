"""Logging module"""

import logging
import os
import sys

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d - %(funcName)s"  # pylint: disable=line-too-long
DATE_FMT = "%d-%b-%y %H:%M:%S"


def init_logging(
    filename="app.log",
    level="INFO",
    log_format=LOG_FORMAT,
    datefmt=DATE_FMT,
    destination="stdout",
):
    """Initialize logging

    Args:
        filename (str, optional): Log file name. Defaults to "app.log".
        level (str, optional): Log level. Defaults to "INFO".
        log_format (str, optional): Log format. Defaults to LOG_FORMAT.
        datefmt (str, optional): Date format. Defaults to "%d-%b-%y %H:%M:%S".
        destination (str, optional): Destination for the logs, can be 'stdout', 'file' or 'both'. Defaults to 'both'.
    """

    log_file = os.environ.get("LOG_FILE", filename)
    log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", level))

    # Create a common formatter that will be used by both handlers
    formatter = logging.Formatter(fmt=log_format, datefmt=datefmt)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    if destination in ("file", "both"):
        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if destination in ("stdout", "both"):
        # Create a stream handler for stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(log_level)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
