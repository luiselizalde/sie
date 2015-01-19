# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint

from app import db
from utils import gen_gui, ArgumentsMissing

administradores = Blueprint('administradores', __name__)

@administradores.route('/administradores', methods=['GET'])
def consulta_general():

	result = Administrador.query.all()

	return jsonify(administradores=result)

@administradores.route('/administradores', methods=['POST'])
def creacion():

	if "administrador" not in request.json:
		raise ArgumentsMissing()


	obj = Administrador(request.json["administrador"])
	created = obj.create()

	return jsonify(administrador=created), 201


@administradores.route('/administradores/<id>', methods=['PUT'])
def modificacion(id):

	obj = Administrador.query.get_or_404(id)

	if "administrador" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["administrador"])

	return jsonify(respuesta="OK")


@administradores.route('/administradores/<id>', methods=['DELETE'])
def eliminacion(id):

	obj = Administrador.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203



class Administrador(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	usuario = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(100))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.usuario = args.get("usuario")
		self.password = args.get("contrasena")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Administrador.query.get(self.id)

		return created

	def update(self, params={}):

		self.usuario = params.get("usuario", self.usuario)
		self.password = params.get("contrasena", self.password)

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def tojson(self):

		dic = {"id":self.id, "usuario":self.usuario}

		return dic




