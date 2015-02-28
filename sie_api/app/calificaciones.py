# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint

from . import db
from utils import gen_gui, ArgumentsMissing
from permisos import permisos, USR_PUB, USR_ADMIN, USR_PROF

calificaciones = Blueprint('calificaciones', __name__)


@calificaciones.route('/calificaciones', methods=['POST'])
@permisos(USR_PROF)
def creacion():

	if "calificacion" not in request.json:
		raise ArgumentsMissing()

	obj = Calificacion(request.json["calificacion"])
	created = obj.create()

	return jsonify(calificacion=created), 201


@calificaciones.route('/calificaciones/<id>', methods=['PUT'])
@permisos(USR_PROF)
def modificacion(id):

	obj = Calificacion.query.get_or_404(id)

	if "calificacion" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["calificacion"])

	return jsonify(respuesta="OK")


@calificaciones.route('/calificaciones/<id>', methods=['DELETE'])
@permisos(USR_PROF)
def eliminacion(id):

	obj = Calificacion.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203



class Calificacion(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	valor = db.Column(db.String(20))
	instrumento = db.Column(db.String(38), db.ForeignKey('instrumento.id'))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.valor = args.get("valor")
		self.instrumento = args.get("instrumento")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Calificacion.query.get(self.id)

		return created

	def update(self, params={}):

		self.valor = params.get("valor")
		self.instrumento = params.get("instrumento")

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def tojson(self):

		dic = {"id":self.id, "valor":self.valor, "instrumento":self.instrumento}

		return dic