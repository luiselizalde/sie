# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint

from app import db
from utils import gen_gui, ArgumentsMissing

parametros = Blueprint('parametros', __name__)


@parametros.route('/parametros', methods=['POST'])
def creacion():

	if "parametro" not in request.json:
		raise ArgumentsMissing()

	obj = Parametro(request.json["parametro"])
	created = obj.create()

	return jsonify(parametro=created), 201


@parametros.route('/parametros/<id>', methods=['PUT'])
def modificacion(id):

	obj = Parametro.query.get_or_404(id)

	if "parametro" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["parametro"])

	return jsonify(respuesta="OK")


@parametros.route('/parametros/<id>', methods=['DELETE'])
def eliminacion(id):

	obj = Parametro.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203


class Parametro(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	nombre = db.Column(db.String(100))
	descripcion = db.Column(db.String(300))
	instrumento = db.Column(db.String(38), db.ForeignKey('instrumento.id'))


	def __init__(self, args={}):
		self.nombre = args.get("nombre")
		self.descripcion = args.get("descripcion")
		self.instrumento = args.get("instrumento")

	def create(self):

		self.id = gen_gui()

		db.session.add(self)
		db.session.commit()

		created = Parametro.query.get(self.id)

		return created

	def update(self, params={}):

		self.nombre = params.get("nombre")
		self.descripcion = params.get("descripcion")
		self.instrumento = params.get("instrumento")

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def tojson(self):

		dic = {"id":self.id, "nombre":self.nombre, "descripcion":self.descripcion, "instrumento":self.instrumento}

		return dic