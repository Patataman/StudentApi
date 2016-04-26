# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from lib.ldapApi import LdapApi
from models.modelos import db, Persona

import jwt, json, lib.Student as Student, datetime

app = Flask(__name__)
app.config.from_pyfile('lib/config.cfg')
db.app = app
db.init_app(app)

#Devolver usuario por nia
@app.route('/student/<int:nia>', methods=['GET'])
def getByNia(nia):
	if check()[0] == 'True':
		students = None
		nia = '(uid=*' + str(nia) + '*)'
		try:
			students = Student.getStudent(nia)
		except Exception as e:
			return 'Demasiados resultados', 500

		#Parsear resultados y return como json
		if students != None:
			if len(students)>1:
				parser = '['
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				return parser
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				return parser
		else:
			return 'Error en la búsqueda', 404
	else:
		return 'BAD AUTHORIZATION', 401

#Devolver usuario por nombre
@app.route('/student/<string:name>', methods=['GET'])
def getByName(name):
	if check()[0] == 'True':
		result = []
		nombre = name.split(",")
		if len(nombre) == 2:
			if nombre[0] != None:
				nombre[0] = nombre[0].strip()
			if nombre[1] != None:
				nombre[1] = nombre[1].strip()
		elif len(nombre) == 1:
			nombre[0] = nombre[0].strip()
		else:
			return 'BAD REQUEST', 400

		if len(nombre) == 2:
			result = '(cn=*' + nombre[0] + ' ' + nombre[1] + '*)'
		elif len(nombre) == 1:
			result = '(cn=*' + nombre[0] + '*)'

		students = None
		try:
			students = Student.getStudent(result)
		except Exception as e:
			return 'Demasiados resultados', 500

		#Parsear resultados y return como json
		if students != None:
			if len(students)>1:
				parser = '['
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				return parser
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				return parser
		else:
			return 'Error en la búsqueda', 404
	else:
		return 'BAD AUTHORIZATION', 401

#Verifica el login y si es correcto, le genera un token
@app.route('/auth', methods=['POST'])
def authorize():
	#Verifica el login y sie
	if login(request.form['nia'], request.form['password'])[0] == 'True':
		persona = Persona.search(request.form['nia'])[0]
		print persona
		payload = {'NIA': request.form['nia'],
					'Nombre':persona.nombre,
					'Apellidos': persona.apellido1 + " " + persona.apellido2,
					'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
		token = jwt.encode(payload, app.config['SECRET'], algorithm='HS256')
		return token
	else:
		return 'False', 400

#Verifica token pasado por header de http
@app.route('/auth', methods=['GET'])
def check():
	r = ['','']
	if request.headers.get('Authorization') != None:
		r = request.headers.get('Authorization').split()
	if r[0] != 'Bearer':
		return 'BAD AUTHORIZATION', 401
	else:
		token = r[1]
		try:
			jwt.decode(token, app.config['SECRET'], algorithms='HS256')
			return 'True', 200
		except Exception as e:
			return 'BAD AUTHORIZATION', 401

#Comprueba si existe el usuario
@app.route('/login', methods=['POST'])
def login(nia=None, password=None):
	ldap = LdapApi(app.config['LDAP_URI'], request.form['nia'], request.form['password'])
	if ldap.auth() == 0:
		if Persona.search(request.form['nia']).count() > 0:
			return 'True', 200
		else:
			return 'BAD AUTHORIZATION', 401
	else:
		return 'False', 400

@app.route('/permisos/<int:nia>/<int:app_id>', methods=['GET'])
def getPermisos(nia, app_id):
	if check()[0] == 'True':
		return str(Permisos.getPermisos(nia,app_id)), 200
	else:
		return 'BAD AUTHORIZATION', 401

@app.route('/delegado/<int:nia>', methods=['GET'])
def getDelegado(nia):
#	if check()[0] == 'True':
#
#	else:
#		return 'BAD AUTHORIZATION', 401
	pass

@app.route('/delegado/isCurso/<int:nia>', methods=['GET'])
def isCurso(nia):
#	if check()[0] == 'True':
#
#	else:
#		return 'BAD AUTHORIZATION', 401
	pass

@app.route('/delegado/isTitulacion/<int:nia>', methods=['GET'])
def isTitulacion(nia):
#	if check()[0] == 'True':
#
#	else:
#		return 'BAD AUTHORIZATION', 401
	pass

@app.route('/delegado/isCentro/<int:nia>', methods=['GET'])
def isCentro(nia):
#	if check()[0] == 'True':
#
#	else:
#		return 'BAD AUTHORIZATION', 401
	pass

if __name__ == '__main__':
	app.run()