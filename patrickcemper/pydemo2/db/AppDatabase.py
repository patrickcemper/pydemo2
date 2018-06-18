############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import logging
from sqlalchemy import create_engine
import random
import string

logger = logging.getLogger(__name__)


class AppDatabase():
    """"This class is responsible for all database interaction. We use a simple SQLITE DB with 2 tables, 'PaymentTransaction' and
    'PrintMessage'. No O/R-mapping is used, just plain SQL to enable the application to persist data."""

    def __init__(self):
        logger.info("Initializing app database 'pydemo2.sqlite'.")
        self.dbEngine = create_engine('sqlite:///pydemo2.sqlite')

    def createDatabase(self):
        conn = self.dbEngine.connect()
        logger.info("Create table PaymentTransaction.")
        conn.execute(
            "create table PaymentTransaction ( "
            "    id                    int      not null primary key, "
            "    record_time           datetime not null, "
            "    transaction_text      text     not null, "
            "    correct_random_number int      null "
            "); ")
        logger.info("Create table PrintMessage.")
        conn.execute(
            "create table PrintMessage ( "
            "    id        int      not null primary key, "
            "    message   text     not null, "
            "    print_ok  int      not null "
            "); ")

    def resetDatabase(self):
        conn = self.dbEngine.connect()
        logger.info("Delete from PaymentTransaction.")
        conn.execute("delete from PaymentTransaction;")
        logger.info("Insert into PaymentTransaction.")
        for i in range(1, 21):
            conn.execute("insert into PaymentTransaction values (?, datetime('now', ?), ?, null); ",
                         i, str(-90+i*3) + " Minutes", "".join([random.choice(string.ascii_letters) for i in range(200)]))
        logger.info("Delete from PrintMessage.")
        conn.execute("delete from PrintMessage;")

    def getNextUnresolvedTransaction(self):
        conn = self.dbEngine.connect()
        query = conn.execute("select id, transaction_text from PaymentTransaction where correct_random_number is null order by id asc;")
        row = query.first()
        if row is None:
            logger.info("No unresolved transactions at the moment.")
            return None
        nextTran = (row[0], row[1])
        logger.info("Next unresolved transaction: {}".format(nextTran))
        return nextTran

    def finishTransaction(self, transId, resultNumber):
        logger.info("Finishing transaction {} with number {}".format(transId, resultNumber))
        conn = self.dbEngine.connect()
        conn.execute("update PaymentTransaction set correct_random_number = ? where id = ?;", resultNumber, transId)

    def getNextPrintMessageId(self):
        conn = self.dbEngine.connect()
        query = conn.execute("select max(id) from PrintMessage;")
        row = query.first()
        nextMessageId = row[0]
        if nextMessageId is None:
            nextMessageId = 1
        else:
            nextMessageId += 1
        logger.info("Next print message ID: {}".format(nextMessageId))
        return nextMessageId

    def initPrintMessage(self, messageId, messageText):
        logger.info("initPrintMessage: {}, {}".format(messageId, messageText))
        conn = self.dbEngine.connect()
        conn.execute("insert into PrintMessage values(?, ?, 0)", messageId, messageText)

    def finishPrintMessage(self, messageId):
        logger.info("finishPrintMessage: {}".format(messageId))
        conn = self.dbEngine.connect()
        conn.execute("update PrintMessage set print_ok = 1 where id = ?", messageId)
