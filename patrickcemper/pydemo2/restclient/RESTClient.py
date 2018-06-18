############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import json
import requests
import logging
from multiprocessing import Process, JoinableQueue, Value
from patrickcemper.pydemo2.worker.ProcessWorker import ProcessWorker
from patrickcemper.pydemo2.worker.SerialMessagePrinter import SerialMessagePrinter
from patrickcemper.pydemo2.worker.SerialMessageWatcher import SerialMessageWatcher


logger = logging.getLogger(__name__)


class RESTClient:
    """This is the client entry point, must be started after server. Via REST calls we get and persists data. This client is
    responsible for managing all worker activity, asnchronous and synchronous ones. Please keep in mind that this is a simple
    demo application and this is definitely not the best or simplest way of doing thing."""

    def __init__(self):
        "Here to init standard parameters for the whole application. For later use."
        logger.info("Initializing pydemo2 client.")
        self.headers = {"Content-Type": "application/json",
                        "User-Agent": "Patrick",
                        "Accept": "application/json"}
        self.messageQueue = JoinableQueue()
        self.answerMessageQueue = JoinableQueue()
        self.currTrans = None
        self.currPrintMessageId = None
        self.searchedNumber = None

    def run(self):
        logger.info("Starting RESTClient.")
        self.getNextUnresolvedTransaction()
        if self.currTrans is not None:
            self.getNextPrintMessageId()
            self.initAsyncSerialMessagePrinter()
            self.initAsyncSerialMessageWatcher()
            self.startSyncProcessWorkers(8)
            self.finishTransaction()
        logger.info("Finishing RESTClient.")

    def getNextUnresolvedTransaction(self):
        logger.info("Getting next unresolved transaction.")
        url = "http://localhost:5002/nextUnresolvedTransaction"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error("Error: HTTP {0} calling {1}.".format(response.status_code, url))
            return
        self.currTrans = json.loads(response.content.decode("UTF-8"))
        if self.currTrans is None:
            logger.info("No unresolved transactions at the moment. Try again later.")
        else:
            logger.info("Found next transaction: {}".format(self.currTrans))

    def getNextPrintMessageId(self):
        logger.info("Getting next print message ID for DB.")
        url = "http://localhost:5002/nextPrintMessageId"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error("Error: HTTP {0} calling {1}.".format(response.status_code, url))
            return
        self.currPrintMessageId = json.loads(response.content.decode("UTF-8"))
        logger.info("Next print message ID for DB: {}".format(self.currPrintMessageId))

    def initAsyncSerialMessagePrinter(self):
        """Asynchronous parallelized special printer worker: Assume it is not locally running and -must- serialize work, e.g. handling
        a printer. It runs immediately and processes the message queue and only stops for a specific STOP. In return it has an
        asynchronous answer queue where another process can check work done in the DB."""
        logger.info("Start init async SerialMessagePrinter.")
        serialMessagePrinter = SerialMessagePrinter()
        process = Process(target=serialMessagePrinter.run, args=(self.messageQueue, self.answerMessageQueue))
        process.daemon = False
        process.start()
        logger.info("Finished init async SerialMessagePrinter.")

    def initAsyncSerialMessageWatcher(self):
        "Watches for answers of async message printer to update DB status."
        logger.info("Start init async SerialMessageWatcher.")
        serialMessageWatcher = SerialMessageWatcher()
        process = Process(target=serialMessageWatcher.run, args=(self.answerMessageQueue,))
        process.daemon = False
        process.start()
        logger.info("Finished init async SerialMessageWatcher.")

    def startSyncProcessWorkers(self, count):
        "Synchronous parallelized workers: They start together and we wait until they finish (all finish when one finishes!)."
        logger.info("Init synced process workers.")
        syncedSearchedNbr = Value('i', 0)
        syncedPrintMsgId = Value('i', self.currPrintMessageId)
        processWorker = ProcessWorker()
        processes = []
        for i in range(count):
            process = Process(target=processWorker.run,
                              args=(i, self.currTrans, syncedSearchedNbr, syncedPrintMsgId, self.messageQueue, self.answerMessageQueue))
            process.daemon = True
            processes.append(process)
            process.start()
        logger.info("Waiting for all processes to finish.")
        for process in processes:
            process.join()
        self.messageQueue.put("STOP")
        self.searchedNumber = syncedSearchedNbr.value
        logger.info("All synced processes finished - result number: {}.".format(self.searchedNumber))

    def finishTransaction(self):
        logger.info("Start finishing transaction {}.".format(self.currTrans[0]))
        url = "http://localhost:5002/finishTransaction"
        response = requests.put(url, params={"transId": self.currTrans[0], "resultNumber": self.searchedNumber}, headers=self.headers)
        if response.status_code != 200:
            logger.error("Error: HTTP {0} calling {1}.".format(response.status_code, url))
            return
        logger.info("End finishing transaction {}.".format(self.currTrans[0]))
