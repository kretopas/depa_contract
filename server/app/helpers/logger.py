# app/helpers/logger.py
from app.config import ROOT_DIR

import os
import logging

LOG_FOLDER_LOCATION = os.path.join(ROOT_DIR, "logs")
LOG_FILE_LOCATION = os.path.join(LOG_FOLDER_LOCATION, "app.log")
logging.basicConfig(filename=LOG_FILE_LOCATION, format='%(asctime)s - %(message)s',
					datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

log = logging.getLogger("app")