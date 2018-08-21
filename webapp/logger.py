# -*- coding: UTF-8 -*-
import logging
import os
import tempfile
from logging.config import dictConfig


LOGGING_CFG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s -- %(levelname)s -- %(message)s'},
        'short': {
            'format': '%(levelname)s: %(message)s'},
        'free': {
            'format': '%(message)s'}},
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 50,
            'filename': os.path.join(tempfile.gettempdir(), 'apiServer.log')},
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'formatter': 'free'}},
    'loggers': {
        'debug': {
            'handlers': ['file'],
            'level': 'DEBUG'},
        'info': {
            'handlers': ['file'],
            'level': 'INFO'},
        'error': {
            'handlers': ['file', 'console'],
            'level': 'ERROR'}}}


def tempfile_name(path, filename):
    if path:
        tempfile.tempdir = path
    if not os.path.exists(tempfile.tempdir):
        os.mkdir(tempfile.tempdir)
    ret = os.path.join(tempfile.gettempdir(), filename)
    if os.access(ret, os.F_OK) and not os.access(ret, os.W_OK):
        print("WARNING: Couldn't write to log file {} "
              "(Permission denied)".format(ret))
        ret = tempfile.mkstemp(prefix='restServer', suffix='.log', text=True)
        print("Create a new log file: {}".format(ret[1]))
        return ret[1]

    return ret


def rest_logger(path, filename, level):
    temp_path = tempfile_name(path, filename)
    if level == 'debug':
        _logger = logging.getLogger('debug')
    elif level == 'info':
        _logger = logging.getLogger('info')
    elif level == 'error':
        _logger = logging.getLogger('error')
    else:
        _logger = logging.getLogger('debug')

    LOGGING_CFG['handlers']['file']['filename'] = temp_path
    dictConfig(LOGGING_CFG)
    return _logger


class Log2file(object):
    def __init__(self, path, filename, level):
        self.__path = path
        self.__filename = filename
        self.__level = level

    def file_loger(self):
        return rest_logger(self.__path, self.__filename, self.__level)


class MyLoger(object):
    MODE_FILE = 'file'

    def __init__(self, path, filename, level):
        self.__file_handler = Log2file(path, filename, level).file_loger()

    def debug(self, data):
        self.__file_handler.debug(data)

    def info(self, data):
        self.__file_handler.info(data)

    def warning(self, data):
        self.__file_handler.warning(data)

    def error(self, data):
        self.__file_handler.error(data)

    def critical(self, data):
        self.__file_handler.critical(data)


log_dir = '/var/log/'
log_name = 'webapp.log'
log_level = 'debug'
logger = MyLoger(log_dir, log_name, log_level)