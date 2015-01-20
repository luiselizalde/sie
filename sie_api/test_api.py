# -*- coding: utf-8 -*-
from requests.api import request

__author__ = 'Luis Elizalde'

import json
import requests

ids = {}
base_url = "http://localhost:1337/"
headers = {'content-type': 'application/json'}

def checkResponse(response, method='GET'):

	print "%s %s : %d" % (method, response.url, response.status_code)

	if response.status_code > 210:

		if response.json():
			print str(response.json())

		raise Exception()

	if response.status_code == 200 and response.json():
		print "\t %s" % str(response.json())

	return response.json()

def test_administradores():

	res_url = base_url + "administradores"
	obj = json.dumps({"administrador" : {"usuario":"super_admin", "contrasena":"1144"}})

	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")


	ids["admin"] = response["administrador"]["id"]

	checkResponse(requests.get(res_url))

	res_url += "/%s" % ids["admin"]

	checkResponse(requests.put(res_url, obj, headers=headers), "PUT")

	#prueba anidada
	test_profesores()

	checkResponse(requests.delete(res_url), "DELETE")


def test_profesores():

	res_url = base_url + "profesores"
	obj = json.dumps({"profesor" : {"usuario":"luis", "contrasena":"4567", "nombre":"Luis Elizalde"}})

	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")

	ids["profesor"] = response["profesor"]["id"]

	checkResponse(requests.get(res_url))

	res_url += "/%s" % ids["profesor"]

	checkResponse(requests.put(res_url, obj, headers=headers), "PUT")

	#prueba anidada
	test_nodos()

	checkResponse(requests.delete(res_url), "DELETE")


def test_nodos():

	res_url = base_url + "nodos"

	obj = json.dumps({"nodo" : {"nombre":"Padre"}})
	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")
	ids["padre"] = response["nodo"]["id"]

	checkResponse(requests.get(res_url))

	obj = json.dumps({"nodo" : {"nombre":"Hijo", "idPadre":ids["padre"]}})
	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")
	ids["hijo"] = response["nodo"]["id"]

	checkResponse(requests.get(res_url, params={"idPadre":ids["padre"]}))

	res_url += "/%s" % ids["hijo"]

	checkResponse(requests.put(res_url, obj, headers=headers), "PUT")

	#prueba anidada
	test_asignaturas()

	checkResponse(requests.get(res_url))
	checkResponse(requests.delete(res_url), "DELETE")
	checkResponse(requests.delete("{0}nodos/{1}".format(base_url, ids["padre"])), "DELETE")


def test_asignaturas():

	res_url = base_url + "asignaturas"

	obj = json.dumps({"asignatura" : {"nombre":"Asignatura 1", "nodo": ids["hijo"], "presidente":ids["profesor"] }})
	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")
	ids["asignatura"] = response["asignatura"]["id"]

	checkResponse(requests.get(res_url, params={"nodo":ids["hijo"]}))


	res_url += "/%s" % ids["asignatura"]

	asignacion_url = res_url + "/profesores"
	asignacion = json.dumps({"profesor" : ids["profesor"]} )
	checkResponse(requests.post(asignacion_url, asignacion, headers=headers), "POST")

	#prueba anidada
	test_instrumentos()

	checkResponse(requests.get(res_url))
	checkResponse(requests.put(res_url, obj, headers=headers), "PUT")

	asignacion_url += "/%s" % ids["profesor"]
	checkResponse(requests.delete(asignacion_url), "DELETE")

	checkResponse(requests.delete(res_url), "DELETE")

def test_instrumentos():

	res_url = base_url + "instrumentos"
	obj = json.dumps({"instrumento" :
		                  {"nombre" : "IE1", "tipo": 1, "asignatura":ids["asignatura"],
		                   "oficial":True, "creador":ids["profesor"]
		                  }})

	response = checkResponse(requests.post(res_url, obj, headers=headers), "POST")

	ids["instrumento"] = response["instrumento"]["id"]

	checkResponse(requests.get(res_url, params={"asignatura":ids["asignatura"]}))

	res_url += "/%s" % ids["instrumento"]

	checkResponse(requests.put(res_url, obj, headers=headers), "PUT")

	#prueba anidada

	checkResponse(requests.get(res_url))

	checkResponse(requests.delete(res_url), "DELETE")


try:
	print "limpiando..."
	checkResponse(requests.get(base_url+"rebuild"))
	print "OK"

	print "Inicia pruebas...."
	test_administradores()
	print "OK"

except Exception as e:
	print e

print ids