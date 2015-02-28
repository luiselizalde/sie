# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from . import db
from flask import request, jsonify, Blueprint
from utils import gen_gui, ArgumentsMissing
from permisos import permisos, USR_PUB, USR_ADMIN, USR_PROF

profesores = Blueprint('profesores', __name__)

@profesores.route('/profesores', methods=['GET'])
@permisos(USR_ADMIN)
def consulta_general():

	result = Profesor.query.all()

	return jsonify(profesores=result)

@profesores.route('/profesores', methods=['POST'])
@permisos(USR_ADMIN)
def creacion():

	if "profesor" not in request.json:
		raise ArgumentsMissing()

	obj = Profesor(request.json["profesor"])
	created = obj.create()

	return jsonify(profesor=created), 201


@profesores.route('/profesores/<id>', methods=['PUT'])
@permisos(USR_ADMIN)
def modificacion(id):

	obj = Profesor.query.get_or_404(id)

	if "profesor" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["profesor"])

	return jsonify(respuesta="OK")


@profesores.route('/profesores/<id>', methods=['DELETE'])
@permisos(USR_ADMIN)
def eliminacion(id):

	obj = Profesor.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203


class Profesor(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	usuario = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(100))
	nombre = db.Column(db.String(100))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.usuario = args.get("usuario")
		self.password = args.get("contrasena")
		self.nombre = args.get("nombre")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Profesor.query.get(self.id)

		return created

	def update(self, params={}):

		self.usuario = params.get("usuario", self.usuario)
		self.password = params.get("contrasena", self.password)
		self.nombre = params.get("nombre", self.nombre)

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def tojson(self):

		dic = {"id":self.id, "usuario":self.usuario, "nombre":self.nombre}

		return dic


