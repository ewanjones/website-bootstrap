"""
 Logging module for printing to the console (Stdout)
"""

import logging

logger = logging.getLogger('root')

def print(message=None):
    """
    Prints a message to the console at the level of INFO
    If the message is none then it will print a newline
    """
    if message:
        logger.info(message)
    else:
        logger.info('\n')

def debug(message):
    """
    Prints a message to the console at the level of DEBUG
    """
    logger.debug(message)

def warn(message):
    """
    Prints a message to the console at the level of WARNING
    """
    logger.warn(message)

def error(message):
    """
    Prints a message to the console at the level of ERROR
    """
    logger.error(message)