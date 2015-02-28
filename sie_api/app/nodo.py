# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint

from . import db
from utils import gen_gui, ArgumentsMissing
from permisos import permisos, USR_PUB, USR_ADMIN, USR_PROF

nodos = Blueprint('nodos', __name__)


@nodos.route('/nodos', methods=['GET'])
@permisos(USR_PUB)
def consulta_general():

	padre = request.args.get("idPadre")
	result = Nodo.query.filter_by(idPadre=padre).all()

	return jsonify(nodos=result)


@nodos.route('/nodos/<id>', methods=['GET'])
@permisos(USR_PUB)
def consulta_detalle(id):

	obj = Nodo.query.get_or_404(id)

	return jsonify(nodo=obj.todjson())

@nodos.route('/nodos', methods=['POST'])
@permisos(USR_ADMIN)
def creacion():

	if "nodo" not in request.json:
		raise ArgumentsMissing()

	obj = Nodo(request.json["nodo"])
	created = obj.create()

	return jsonify(nodo=created), 201


@nodos.route('/nodos/<id>', methods=['PUT'])
@permisos(USR_ADMIN)
def modificacion(id):

	obj = Nodo.query.get_or_404(id)

	if "nodo" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["nodo"])

	return jsonify(respuesta="OK")


@nodos.route('/nodos/<id>', methods=['DELETE'])
@permisos(USR_ADMIN)
def eliminacion(id):

	obj = Nodo.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203

class Nodo(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	nombre = db.Column(db.String(100))
	idPadre = db.Column(db.String(38), db.ForeignKey('nodo.id'))

	def __init__(self, args={}):
		self.id = gen_gui()
		self.nombre = args.get("nombre")
		self.idPadre = args.get("idPadre")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Nodo.query.get(self.id)

		return created

	def update(self, params={}):

		self.nombre = params.get("nombre", self.nombre)
		self.idPadre = params.get("idPadre", self.idPadre)

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def todjson(self):

		from asignatura import Asignatura

		dic = self.tojson()
		dic["hijos"] = Nodo.query.filter_by(idPadre=self.id).all()
		dic["asignaturas"] = Asignatura.query.filter_by(nodo=self.id).all()

		return dic

	def tojson(self):

		dic = {"id":self.id, "nombre":self.nombre, "idPadre": self.idPadre}

		return dic
