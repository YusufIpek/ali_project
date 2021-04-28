import logging
import logging.handlers
from datetime import date
import utils

utils.create_folder_if_not_exist("logs")

logger = logging.getLogger("main")

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/logs-" + str(date.today()) + ".log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
