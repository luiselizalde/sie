#-*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

from utils import gen_gui, CustomJSONEncoder, ArgumentsMissing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost/sie"
app.json_encoder = CustomJSONEncoder

db = SQLAlchemy(app)


from detalle import detalles
from admin import  administradores
from profesor import profesores
from asignatura import asignaturas
from calificaciones import calificaciones
from instrumento import instrumentos
from nodo import nodos
from parametro import parametros


app.register_blueprint(profesores)
app.register_blueprint(detalles)
app.register_blueprint(administradores)
app.register_blueprint(asignaturas)
app.register_blueprint(calificaciones)
app.register_blueprint(instrumentos)
app.register_blueprint(nodos)
app.register_blueprint(parametros)


@app.route('/')
def hello_world():
	return 'Hello World!'

@app.after_request
def after_request(response):

	print "%s %s - %d " % (request.url_rule, request.json, response.status_code)

	return response

@app.before_request
def before_request():

	if request.method in ['POST', 'PUT']:

		if not request.json:
			raise ArgumentsMissing()


@app.route('/rebuild')
def rebuild():

	from admin import Administrador

	db.drop_all()

	db.create_all()

	a = Administrador({"usuario":"admin", "contrasena":"1234"})

	db.session.add(a)
	db.session.commit()

	return jsonify(respuesta = "OK")

@app.errorhandler(ArgumentsMissing)
def ArgumentsMissing_handler(error):
	return jsonify(respuesta="Esta petición requiere parametros"), 400

@app.errorhandler(Exception)
def error_handler(error):
	return jsonify(respuesta=str(error)), 500