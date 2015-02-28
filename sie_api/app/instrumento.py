# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

import datetime

from flask import request, jsonify, Blueprint, g

from . import db
from utils import gen_gui, ArgumentsMissing
from permisos import permisos, USR_PUB, USR_ADMIN, USR_PROF


instrumentos = Blueprint('instrumentos', __name__)


@instrumentos.route('/instrumentos', methods=['GET'])
@permisos(USR_PUB)
def consulta_general():

	if "asignatura" not in request.args:
		raise ArgumentsMissing()

	result = Instrumento.query.filter_by(asignatura=request.args["asignatura"]).all()

	return jsonify(instrumentos=result)


@instrumentos.route('/instrumentos/<id>', methods=['GET'])
@permisos(USR_PUB)
def consulta_detalle(id):

	obj = Instrumento.query.get_or_404(id)

	return jsonify(instrumento=obj.todjson())

@instrumentos.route('/instrumentos', methods=['POST'])
@permisos(USR_PROF)
def creacion():

	if "instrumento" not in request.json:
		raise ArgumentsMissing()

	obj = Instrumento(request.json["instrumento"])
	created = obj.create()

	return jsonify(instrumento=created), 201


@instrumentos.route('/instrumentos/<id>', methods=['PUT'])
@permisos(USR_PROF)
def modificacion(id):

	obj = Instrumento.query.get_or_404(id)

	if "instrumento" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["instrumento"])

	return jsonify(respuesta="OK")


@instrumentos.route('/instrumentos/<id>', methods=['DELETE'])
@permisos(USR_PROF)
def eliminacion(id):

	obj = Instrumento.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203


class Instrumento(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	nombre = db.Column(db.String(100))
	tipo = db.Column(db.Integer)
	asignatura = db.Column(db.String(38), db.ForeignKey('asignatura.id'))
	oficial = db.Column(db.Boolean)
	creador = db.Column(db.String(38), db.ForeignKey('profesor.id'))
	fecha = db.Column(db.String(20))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.nombre = args.get("nombre")
		self.tipo = args.get("tipo")
		self.asignatura = args.get("asignatura")
		self.oficial = args.get("oficial")

		self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.creador = g.session.user_id

	def create(self):


		db.session.add(self)
		db.session.commit()

		created = Instrumento.query.get(self.id)

		return created

	def update(self, params={}):

		self.nombre = params.get("nombre", self.nombre)
		self.tipo = params.get("tipo", self.tipo)
		self.asignatura = params.get("asignatura", self.asignatura)
		self.oficial = params.get("oficial", self.oficial)


		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def todjson(self):

		from detalle import Detalle
		from parametro import Parametro
		from calificaciones import Calificacion

		dic = self.tojson()
		dic["asignatura"] = self.asignatura
		dic["creador"] = self.creador
		dic["fecha"] = self.fecha

		dic["detalles"] = Detalle.query.filter_by(instrumento=self.id).all()
		dic["parametros"] = Parametro.query.filter_by(instrumento=self.id).all()
		dic["calificaciones"] = Calificacion.query.filter_by(instrumento=self.id).all()

		return dic

	def tojson(self):

		dic = {"id":self.id, "nombre":self.nombre, "tipo":self.tipo, "oficial":self.oficial}

		return dic