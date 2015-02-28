# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, g

USR_PUB = 'N'
USR_PROF = 'A'
USR_ADMIN = 'P'

def permisos(*roles):

	def permisos_decorator(f):

		if USR_PUB in roles:
			return f

		def wrapper(*args,**kwargs):

			from session import Session

			auth = request.headers.get('Authorization')

			if not auth:
				return ("Usuario no ha iniciado sesión"), 401

			token = str(auth)

			session = Session.query.get(token)

			if not session:
				return ("Token invalido"), 401

			if not session.isValid():
				return ("Token expiró"), 401

			if session.user_type not in roles:
				return ("Acceso restringido"), 403

			g.session = session

			return f(*args, **kwargs)

		wrapper.__name__ = f.__name__

		return wrapper

	return permisos_decorator