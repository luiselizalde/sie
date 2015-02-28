# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from datetime import datetime


from flask import request, jsonify, Blueprint, g

from . import db
from utils import gen_gui, ArgumentsMissing
from permisos import permisos, USR_PUB, USR_ADMIN, USR_PROF

from admin import Administrador
from profesor import Profesor


session = Blueprint('sessions', __name__)


@session.route('/login', methods=['POST'])
@permisos(USR_PUB)
def login():

	username = request.json.get('usuario')
	password = request.json.get('contrasena')

	if not username or not password:
		raise ArgumentsMissing()

	user = Profesor.query.filter_by(usuario=username).first()

	if not user:
		user = Administrador.query.filter_by(usuario=username).first_or_404()

	if user.password != password:
		return 'Usuario o contraseña incorrectos', 401


	user_type = USR_PROF if hasattr(user, 'nombre') else USR_ADMIN

	new_session = Session(user.id, user_type)
	new_session = new_session.create()

	return jsonify(token=new_session.token)


@session.route('/refresh', methods=['GET'])
@permisos(USR_PROF, USR_ADMIN)
def refresh():
	return jsonify(respuesta="OK"), 200


@session.route('/logout', methods=['DELETE'])
@permisos(USR_PROF, USR_ADMIN)
def logout():

	g.session.delete()

	return jsonify(respuesta="OK"), 200


class Session(db.Model):

	SESSION_EXPIRATION = 900

	token =  db.Column(db.String(38), primary_key=True)
	user_id = db.Column(db.String(38))
	user_type = db.Column(db.String(1))
	last_transaction = db.Column(db.DateTime)

	def __init__(self, user_id, user_type):

		self.token = gen_gui()
		self.last_transaction = datetime.now()

		self.user_id = user_id
		self.user_type = user_type


	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Session.query.get(self.token)

		return created

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def isValid(self):

		n = datetime.now()
		diff = n - self.last_transaction

		if diff.total_seconds() < self.SESSION_EXPIRATION:

			self.last_transaction = n
			db.session.commit()

			return True

		self.delete()






