# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import request, jsonify, Blueprint, g


from app import db
from utils import gen_gui, ArgumentsMissing


from sqlalchemy import and_

asignaturas = Blueprint('asignaturas', __name__)


@asignaturas.route('/asignaturas', methods=['GET'])
def consulta_general():

	if "nodo" not in request.args:
		raise ArgumentsMissing()

	result = Asignatura.query.filter_by(nodo=request.args["nodo"]).all()

	return jsonify(asignaturas=result)


@asignaturas.route('/asignaturas/<id>', methods=['GET'])
def consulta_detalle(id):

	obj = Asignatura.query.get_or_404(id)

	return jsonify(asignatura=obj.todjson())

@asignaturas.route('/asignaturas', methods=['POST'])
def creacion():

	if "asignatura" not in request.json:
		raise ArgumentsMissing()

	obj = Asignatura(request.json["asignatura"])
	created = obj.create()

	return jsonify(asignatura=created), 201


@asignaturas.route('/asignaturas/<id>', methods=['PUT'])
def modificacion(id):

	obj = Asignatura.query.get_or_404(id)

	if "asignatura" not in request.json:
		raise ArgumentsMissing()

	obj.update(request.json["asignatura"])

	return jsonify(respuesta="OK")


@asignaturas.route('/asignaturas/<id>', methods=['DELETE'])
def eliminacion(id):

	obj = Asignatura.query.get_or_404(id)
	obj.delete()

	return jsonify(respuesta="OK"), 203

@asignaturas.route('/asignaturas/<id>/profesores', methods=['POST'])
def asignar_profesor(id):

	if "profesor" not in request.json:
		raise ArgumentsMissing()

	obj = AsignacionProfesor(asignatura=id, profesor=request.json["profesor"])
	obj.create()

	return jsonify(respuesta="OK"), 201


@asignaturas.route('/asignaturas/<idA>/profesores/<idP>', methods=['DELETE'])
def quitar_profesor(idP, idA):

	res = AsignacionProfesor.query.filter_by(asignatura=idA).all()

	for r in res:
		if r.profesor == idP:
			r.delete()
			return jsonify(respuesta="OK"), 203

	return jsonify(respuesta="No encontrado"), 404


class Asignatura(db.Model):

	id = db.Column(db.String(38), primary_key=True)
	nombre = db.Column(db.String(100))
	nodo = db.Column(db.String(38), db.ForeignKey('nodo.id'))
	presidente = db.Column(db.String(38), db.ForeignKey('profesor.id'))


	def __init__(self, args={}):
		self.id = gen_gui()
		self.nombre = args.get("nombre")
		self.nodo = args.get("nodo")
		self.presidente = args.get("presidente")

	def create(self):

		db.session.add(self)
		db.session.commit()

		created = Asignatura.query.get(self.id)

		return created

	def update(self, params={}):

		self.nombre = params.get("nombre", self.nombre)
		self.nodo = params.get("nodo", self.nodo)
		self.presidente = params.get("presidente", self.presidente)

		db.session.commit()

	def delete(self):

		db.session.delete(self)
		db.session.commit()

	def todjson(self):

		from profesor import Profesor
		from instrumento import Instrumento

		dic = self.tojson()

		dic["nodo"] = self.nodo
		dic["presidente"] = self.presidente
		dic["instrumentos"] = Instrumento.query.filter_by(asignatura=self.id).all()
		dic["profesores"] = []

		profs = AsignacionProfesor.query.filter_by(asignatura=self.id).all()

		for p in profs:

			res = Profesor.query.get(p.profesor)

			if res:
				dic["profesores"].append(res.tojson())

		return dic

	def tojson(self):

		dic = {"id":self.id, "nombre":self.nombre}

		return dic


class AsignacionProfesor(db.Model):

	asignatura = db.Column(db.String(38), db.ForeignKey('asignatura.id'), primary_key=True)
	profesor = db.Column(db.String(38), db.ForeignKey('profesor.id'), primary_key=True)

	def __init__(self, asignatura, profesor):
		self.asignatura = asignatura
		self.profesor = profesor

	def create(self):

		db.session.add(self)
		db.session.commit()


	def delete(self):

		db.session.delete(self)
		db.session.commit()


	def tojson(self):

		dic = {"asignatura":self.asignatura, "profesor":self.profesor}

		return dic