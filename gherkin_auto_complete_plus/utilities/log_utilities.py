import functools
import logging


def log_function(logging_level):
    """ Logs function information -- sets logging level to provided level """
    def inner_log_func(func):
        @functools.wraps(inner_log_func)
        def wrap(*args, **kwargs):

            logger = logging.getLogger(func.__module__)
            logger.setLevel(logging_level)
            logger.info('Entering function "{}"'.format(func.__name__))

            f_result = func(*args, **kwargs)
            logger.debug('{} result: {}'.format(func.__name__, f_result))

            logger.info('Exiting "{}"'.format(func.__name__))
            return f_result
        return wrap
    return inner_log_func


def get_logger(module_name, logging_level):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging_level)
    return logger
