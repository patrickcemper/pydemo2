############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import logging
import random
from datetime import datetime
from patrickcemper.pydemo2.base import Globals


logger = logging.getLogger(__name__)


class ProcessWorker():
    """Processes the actual proof of work for an transaction (of course just simulated here via a random number generator combined with
    a loop). Several of these process workers run in synchronous parallel and try to find a result below 100, basically in the style
    of a blockchain miner sortof. With a lot of fantasy I guess. :-)
    To make things a little more interesting we also notify a hypthetical serial print process every time we are close. Since these
    messages are important we keep track of them via the serial watcher and the answerQueue and an own database table that tracks
    wheather a message was really sucessfully printed (with init and OK status). This back and forth via queues all itself happens via
    queues and asynchronous."""

    def run(self, processId, currTrans, syncedSearchedNbr, syncedPrintMsgId, messageQueue, answerMessageQueue):
        starttime = datetime.now()
        logger.info("[Process {}] Starting for transaction id {} - {}[...].".format(processId, currTrans[0], currTrans[1][:20]))

        # So a pseudo calculation until a result value is below 100.
        randresult = 100
        while randresult >= 100 and syncedSearchedNbr.value == 0:
            randresult = random.randint(1, Globals.PROCESSING_DIFFICULTY)
            # If the number is close to 100 (below 1000), print a message. This happens asynchronous via a message queue.
            if randresult >= 100 and randresult < 1000:
                currPrintMessageId = None
                with syncedPrintMsgId.get_lock():
                    currPrintMessageId = syncedPrintMsgId.value
                    syncedPrintMsgId.value += 1
                currMessage = ("[{}] [msgId{:3d}] [from process {}] For transaction id {}: Important notification! Almost below "
                               "100: {}.".format(datetime.now(), currPrintMessageId, processId, currTrans[0], randresult))
                answerMessageQueue.put((currPrintMessageId, currMessage))
                messageQueue.put((currPrintMessageId, currMessage))

        # Finish psyeudo calculation, signal the other workers to stop. Take any number as searched number - doesn't matter for demo.
        if randresult < 100:
            with syncedSearchedNbr.get_lock():
                syncedSearchedNbr.value = random.randint(1, 1000000000)
            timediffsec = (datetime.now() - starttime).total_seconds()
            logger.info("[Process {}] Success after {} sec - searched number: {}".format(processId, timediffsec, syncedSearchedNbr.value))
        else:
            logger.info("[Process {}] Aborted - other process was faster.".format(processId))
