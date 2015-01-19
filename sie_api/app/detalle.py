# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint, g

from app import db
from utils import gen_gui, ArgumentsMissing


detalles = Blueprint('detalles', __name__)


@detalles.route('/detalles', methods=['POST'])
def creacion():

	if "detalle" not in request.json:
		raise ArgumentsMissing()

	obj = Detalle(request.json["detalle"])
	created = obj.create()

	return jsonify(detalle=created), 201


@detalles.route('/detalles/<id>', methods=['PUT'])
def modificacion(id):

	obj = Detalle.query.get_or_404(id)

	if "detalle" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["detalle"])

	return jsonify(respuesta="OK")


@detalles.route('/detalles/<id>', methods=['DELETE'])
def eliminacion(id):

	obj = Detalle.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203



class Detalle(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	parametro = db.Column(db.String(38), db.ForeignKey('parametro.id'))
	calificacion = db.Column(db.String(38), db.ForeignKey('calificacion.id'))
	detalle = db.Column(db.String(300))
	instrumento = db.Column(db.String(38), db.ForeignKey('instrumento.id'))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.parametro = args.get("parametro")
		self.calificacion = args.get("calificacion")
		self.detalle = args.get("detalle")
		self.instrumento = args.get("instrumento")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Detalle.query.get(self.id)

		return created

	def update(self, params={}):

		self.parametro = params.get("parametro")
		self.calificacion = params.get("calificacion")
		self.detalle = params.get("detalle")
		self.instrumento = params.get("instrumento")

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def tojson(self):

		dic = {"id":self.id, "parametro":self.parametro, "calificacion":self.calificacion, "detalle":self.detalle, "instrumento":self.instrumento}

		return dic