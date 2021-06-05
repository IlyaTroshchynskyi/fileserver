import logging
import logging.handlers
import os

ONE_MB = 1_000_000
TEST_FILES_DIR = 'test_files'
FILES_PER_PAGE = 5


def init_logger(name):
    """Init logger for application. Set formats for writing information to the files and
    for output to debug.
    Args:
        name (srt): name of root logger
    """
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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fileserver.db'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

