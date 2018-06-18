####################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
####################################################################################################
#
# Order to execute the main modules:
#   (1) main_createdb.py (Only if .sqlite-file does not yet exist.)
#   (2) main_restdb.py
#   (3) main_server.py
#   (4) main_client.py
#
####################################################################################################
#
# Application Description
#
# A little demo application I threw together to ge into Python and to play around with:
# - REST services (server + client code)
# - synchronous multiprocessing
# - asynchronous multiprocessing
# - message queues
# - logging
# - simple SQL handling
# - ...have some fun! :-)
#
####################################################################################################
#
# Class Description
#
# class AppDatabase():
#     """"This class is responsible for all database interaction. We use a simple SQLITE DB with
#     2 tables, 'PaymentTransaction' and 'PrintMessage'. No O/R-mapping is used, just plain SQL
    to enable the application to persist data."""
#
# class RESTServer():
#     "Provides REST services required in this app and connects with the database."
#
# class RESTClient:
#     """This is the client entry point, must be started after server. Via REST calls we get and
#     persists data. This client is responsible for managing all worker activity, asnchronous and
#     synchronous ones. Please keep in mind that this is a simple demo application and this is
#     definitely not the best or simplest way of doing thing."""
#
# class ProcessWorker():
#     """Processes the actual proof of work for an transaction (of course just simulated here via
#     a random number generator combined with a loop). Several of these process workers run in
#     synchronous parallel and try to find a result below 100, basically in the style of a
#     blockchain miner sortof. With a lot of fantasy I guess. :-) To make things a little more
#     interesting we also notify a hypthetical serial print process every time we are close. Since
#     these messages are important we keep track of them via the serial watcher and the
#     answerQueue and an own database table that tracks wheather a message was really sucessfully
#     printed (with init and OK status). This back and forth via queues all itself happens via
#     queues and asynchronous."""
#
# class SerialMessagePrinter():
#     """This is the serial printer process. It receives messages asynchronously via a message
#     queue and processes them, slowly in this simulation because we assume it is a physical
#     decise that takes serveral seconds."""
#
# class SerialMessageWatcher():
#     """This class is the asynchronous counter part of the serial message printer. It does two
#     things: it keeps track of the initial occurance of an important printable message, and when
#     the printer is done we get an OK and update this status in the DB. As said before this is
#     extremely overcomplicated and just here for the sake of demonstrating several communication
#     paradigms between applications / processes."""
#
# def Globals.init():
#     """This is the init method for global constants. Please feel free to modify these in case
#     your machine doesn't work as fast or as slow as mine. PROCESSING_DIFFICULTY must be
#     increased when the workers find the result too fast, otherwise it must be decreased.
#     PRINTING_TIME should stay rather high so we see the wanted effect of after-work when all is
#     found for the transaction but message printing and tracking is still ongoing."""
#
####################################################################################################
#
# Used
#
# - Python 3.6.5
# - Sqlite 3.24.0
#
####################################################################################################
#
# pip freeze (not all needed I guess..)
#
# aniso8601==3.0.2
# autopep8==1.3.5
# certifi==2018.4.16
# chardet==3.0.4
# click==6.7
# Flask==1.0.2
# Flask-Jsonpify==1.5.0
# Flask-RESTful==0.3.6
# Flask-SQLAlchemy==2.3.2
# future==0.16.0
# idna==2.7
# itsdangerous==0.24
# jedi==0.12.0
# Jinja2==2.10
# MarkupSafe==1.0
# marshmallow==2.15.3
# mccabe==0.6.1
# parso==0.2.1
# pluggy==0.6.0
# pycodestyle==2.4.0
# pydocstyle==2.1.1
# pyflakes==2.0.0
# python-language-server==0.19.0
# pytz==2018.4
# requests==2.19.1
# rope==0.10.7
# six==1.11.0
# snowballstemmer==1.2.1
# SQLAlchemy==1.2.8
# urllib3==1.23
# webargs==3.0.1
# Werkzeug==0.14.1
# yapf==0.22.0
#
####################################################################################################
