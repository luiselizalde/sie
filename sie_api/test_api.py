# -*- coding: utf-8 -*-
__author__ = 'Luis Elizalde'

import json
import requests

base_url = "http://localhost:1337/"
headers = {'content-type': 'application/json'}

def checkResponse(response):

	print "%s : %d" % (response.url, response.status_code)

	if response.status_code > 210:
		raise Exception()

	return response.json()

def test_administradores():

	print "Inicia prueba de administradores...."

	admin_url = base_url + "administradores"
	admin = json.dumps({"administrador" : {"usuario":"luis", "contrasena":"1144"}})


	response = checkResponse(requests.post(admin_url, admin, headers=headers))

	checkResponse(requests.get(admin_url))

	admin_url += "/%s" % response["administrador"]["id"]

	checkResponse(requests.put(admin_url, admin, headers=headers))
	checkResponse(requests.delete(admin_url))

	print "OK"

try:
	print "limpiando..."
	checkResponse(requests.get(base_url+"rebuild"))
	print "OK"

	test_administradores()
except Exception as e:
	print e
