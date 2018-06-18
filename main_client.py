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
from patrickcemper.pydemo2.restclient.RESTClient import RESTClient
from patrickcemper.pydemo2.base.Globals import init as initGlobals


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
initGlobals()

# This IF is required to make multiprocessing acutally work on Windows (to prevent recursive process invocation).
if __name__ == "__main__":
    logger.info("Starting main_client.")
    client = RESTClient()
    client.run()
    logger.info("Finishing main_client.")
