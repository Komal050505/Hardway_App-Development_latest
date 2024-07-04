from app_development.logging_activity.logging_module import logging
from app_development.app.constants import LOG_SWITCH


def log_info(message):
    if LOG_SWITCH:
        logging.info(message)


def log_debug(message):
    if LOG_SWITCH:
        logging.debug(message)


def log_error(message):
    if LOG_SWITCH:
        logging.error(message)


def log_warning(message):
    if LOG_SWITCH:
        logging.warning(message)
