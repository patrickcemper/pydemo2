############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################
#
# Order to execute the main modules:
#   (1) main_createdb.py (Only if .sqlite-file does not yet exist.)
#   (2) main_restdb.py
#   (3) main_server.py
#   (4) main_client.py
#
# See readme.txt for installation instructions and a short summary of what this application is about!
#
############################################################################################################################################

import logging
from patrickcemper.pydemo2.db.AppDatabase import AppDatabase


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


logger.info("Starting main_resetdb.")
appDatabase = AppDatabase()
appDatabase.resetDatabase()
logger.info("Finishing main_resetdb.")
