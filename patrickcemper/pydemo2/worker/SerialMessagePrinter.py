############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import logging
from datetime import datetime
import time
from patrickcemper.pydemo2.base import Globals

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("SerialMessagePrinter.log"))
logger.propagate = False


class SerialMessagePrinter():
    """This is the serial printer process. It receives messages asynchronously via a message queue and processes them, slowly in this
    simulation because we assume it is a physical decise that takes serveral seconds."""

    def run(self, messageQueue, answerMessageQueue):
        logger.info("[{}] Starting to print messages from queue.".format(datetime.now()))

        message = None
        while message != "STOP":
            message = messageQueue.get()
            if message == "STOP":
                # Stop answer message queue as well if stopped.
                answerMessageQueue.put("STOP")
            else:
                # arbitrary wait time of 1 sec to simulate the printer.
                time.sleep(Globals.PRINTING_TIME)
                # print text part of message to a log file. Addactual printing time!
                logger.info("[{}] {}".format(datetime.now(), message[1]))
                # Notify the RESTClient that the message was safely "printed" via answer message queue.
                answerMessageQueue.put((message[0], "OK"))

        logger.info("[{}] Finished printing messages from queue.".format(datetime.now()))
