#-*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

import os

import logging
import logging.handlers

from cherrypy import wsgiserver
from paste.translogger import TransLogger

from app import app

APP_FOLDER = os.path.dirname(os.path.realpath(__file__))
LOG_FOLDER = APP_FOLDER + '/log'

if not os.path.exists(LOG_FOLDER):
	os.mkdir(LOG_FOLDER)

formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

handler = logging.handlers.TimedRotatingFileHandler(LOG_FOLDER+"/error.log", when="midnight", backupCount = 7)
handler.setLevel(logging.ERROR)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)

port = 1337
wsgi_app = TransLogger(app, logger_name="root", setup_console_handler=False)

d = wsgiserver.WSGIPathInfoDispatcher({'/': wsgi_app})
server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', port), d)


if __name__ == "__main__":

	try:
		print "sie api en puerto : %d ..." % port
		server.start()
	except KeyboardInterrupt:
		server.stop()