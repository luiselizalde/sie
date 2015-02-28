# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'


import datetime

from flask.json import JSONEncoder

def gen_gui():
	import uuid
	gui = uuid.uuid4().hex.upper()
	return gui

class ArgumentsMissing(Exception):
	pass

class CustomJSONEncoder(JSONEncoder):

	def default(self, obj):
		if isinstance(obj, datetime.date):
			return obj.isoformat()
		try:
			return obj.tojson()
		except AttributeError:
			return JSONEncoder.default(self, obj)
