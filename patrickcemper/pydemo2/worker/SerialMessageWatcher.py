############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import logging
import requests
from datetime import datetime


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("SerialMessageWatcher.log"))
logger.propagate = False


class SerialMessageWatcher():
    """This class is the asynchronous counter part of the serial message printer. It does two things: it keeps track of the initial
    occurance of an important printable message, and when the printer is done we get an OK and update this status in the DB. As
    said before this is extremely overcomplicated and just here for the sake of demonstrating several communication paradigms between
    applications / processes."""

    def __init__(self):
        self.headers = {"Content-Type": "application/json",
                        "User-Agent": "Patrick",
                        "Accept": "application/json"}

    def run(self, answerMessageQueue):
        logger.info("[{}] Starting waiting for serial printer response.".format(datetime.now()))

        message = None
        while message != "STOP":
            message = answerMessageQueue.get()
            if message != "STOP" and len(message) == 2:
                if message[1] == "OK":
                    logger.info("[{}] Print message ID {}: OK".format(datetime.now(), message[0]))
                    self.finishPrintMessageInDB(message[0])
                else:
                    logger.info("[{}] Print message ID {}: INIT: {}".format(datetime.now(), message[0], message[1]))
                    self.initPrintMessageInDB(message[0], message[1])

        logger.info("[{}] Finished waiting for serial printer response.".format(datetime.now()))

    def initPrintMessageInDB(self, messageId, messageText):
        url = "http://localhost:5002/initPrintMessage"
        response = requests.put(url, params={"messageId": messageId, "messageText": messageText}, headers=self.headers)
        if response.status_code != 200:
            logger.error("[{}] Error: HTTP {0} calling {1}.".format(datetime.now(), response.status_code, url))

    def finishPrintMessageInDB(self, messageId):
        url = "http://localhost:5002/finishPrintMessage"
        response = requests.put(url, params={"messageId": messageId}, headers=self.headers)
        if response.status_code != 200:
            logger.error("[{}] Error: HTTP {0} calling {1}.".format(datetime.now(), response.status_code, url))
