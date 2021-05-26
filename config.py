import logging
import logging.handlers
import os

ONE_MB = 1000000
TEST_FILES_DIR = 'test_files'

def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s ' \
             '- FUNCTION=%(funcName)s - %(message)s'
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    sh.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(filename='file_server.log',
                                              maxBytes=10*ONE_MB, backupCount=100)
    fh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.info("Logger was initialized")


class Configuration:

    SECRET_KEY = 'something_very_secret'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), TEST_FILES_DIR)
    ALLOWED_EXTENSIONS = {'txt', 'xlsx', 'json', 'csv'}