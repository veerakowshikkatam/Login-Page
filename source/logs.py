import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="loggers_file.log", level = logging.DEBUG, format ="%(asctime)s:%(levelname)s%(name)s:%(message)s")
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)