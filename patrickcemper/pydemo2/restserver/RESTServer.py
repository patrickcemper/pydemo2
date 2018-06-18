############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################

import logging
from flask import Flask
from pprint import pformat
from flask_restful import Resource, Api, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask import jsonify
from patrickcemper.pydemo2.db.AppDatabase import AppDatabase


logger = logging.getLogger(__name__)
appDatabase = AppDatabase()


@parser.error_handler
def handleParsingError(error, request):
    logger.error("Request parsing error: " + pformat(error.messages))
    logger.error("Request: " + pformat(request))
    abort(422, errors=error.messages)


class RESTServer():
    "Provides REST services required in this app and connects with the database."

    def run(self):
        serverApp = Flask(__name__)
        serverApi = Api(serverApp)
        serverApi.add_resource(NextUnresolvedTransaction, "/nextUnresolvedTransaction")
        serverApi.add_resource(FinishTransaction, "/finishTransaction")
        serverApi.add_resource(NextPrintMessageId, "/nextPrintMessageId")
        serverApi.add_resource(InitPrintMessage, "/initPrintMessage")
        serverApi.add_resource(FinishPrintMessage, "/finishPrintMessage")
        serverApp.run(port='5002')


class NextUnresolvedTransaction(Resource):
    def get(self):
        logger.info("Calling /nextUnresolvedTransaction (GET).")
        nextTran = appDatabase.getNextUnresolvedTransaction()
        if nextTran is None:
            return None
        return jsonify(nextTran)


class FinishTransaction(Resource):
    args = {
        "transId": fields.Int(
            required=True,
            validate=validate.Range(min=1)
        ),
        "resultNumber": fields.Int(
            required=True,
            validate=validate.Range(min=1)
        )
    }

    @use_kwargs(args)
    def put(self, transId, resultNumber):
        logger.info("Calling /finishTransaction (PUT) with transId={}, resultNumber={}.".format(transId, resultNumber))
        appDatabase.finishTransaction(transId, resultNumber)


class NextPrintMessageId(Resource):
    def get(self):
        logger.info("Calling /nextPrintMessageId (GET).")
        nextMessageId = appDatabase.getNextPrintMessageId()
        return jsonify(nextMessageId)


class InitPrintMessage(Resource):
    args = {
        "messageId": fields.Int(
            required=True,
            validate=validate.Range(min=1)
        ),
        "messageText": fields.Str(
            required=True
        )
    }

    @use_kwargs(args)
    def put(self, messageId, messageText):
        logger.info("Calling /initPrintMessage (PUT).")
        appDatabase.initPrintMessage(messageId, messageText)


class FinishPrintMessage(Resource):
    args = {
        "messageId": fields.Int(
            required=True,
            validate=validate.Range(min=1)
        )
    }

    @use_kwargs(args)
    def put(self, messageId):
        logger.info("Calling /finishPrintMessage (PUT).")
        appDatabase.finishPrintMessage(messageId)
