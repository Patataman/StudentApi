# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from lib.ldapApi import LdapApi
from models.modelos import db, Persona

import jwt, json, lib.Student as Student, datetime

app = Flask(__name__)
app.config.from_pyfile('lib/config.cfg')
db.app = app
db.init_app(app)

@app.route('/')
def index():
	resp = Response(status=200)
	resp.headers['respuesta'] = 'True'
	return resp

#Devolver usuario por nia
@app.route('/student/<int:nia>', methods=['GET'])
def getByNia(nia):
	if check().headers['respuesta'] == 'True':
		students = None
		nia = '(uid=*' + str(nia) + '*)'
		try:
			students = Student.getStudent(nia)
		except Exception as e:
			resp = Response(status=500)
			resp.headers['respuesta'] = False
			return resp

		#Parsear resultados y return como json
		if students != None:
			if len(students)>1:
				parser = '['
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				resp = Response(status=200)
				resp.headers['respuesta'] = parser
				return resp
				#return parser
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				resp = Response(status=200)
				resp.headers['respuesta'] = parser
				return resp
				#return parser
		else:
			resp = Response(status=404)
			resp.headers['respuesta'] = False
	else:
		resp = Response(status=401)
		resp.headers['respuesta'] = False

#Devolver usuario por nombre
@app.route('/student/<string:name>', methods=['GET'])
def getByName(name):
	if check().headers['respuesta'] == 'True':
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
			resp = Response(status=406)
			resp.headers['respuesta'] = False

		if len(nombre) == 2:
			result = '(cn=*' + nombre[0] + ' ' + nombre[1] + '*)'
		elif len(nombre) == 1:
			result = '(cn=*' + nombre[0] + '*)'

		students = None
		try:
			students = Student.getStudent(result)
		except Exception as e:
			resp = Response(status=500)
			resp.headers['respuesta'] = False
			return resp

		#Parsear resultados y return como json
		if students != None:
			if len(students)>1:
				parser = '['
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				resp = Response(status=200)
				resp.headers['respuesta'] = parser
				return resp
				#return parser
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				resp = Response(status=200)
				resp.headers['respuesta'] = parser
				return resp
				#return parser
		else:
			resp = Response(status=404)
			resp.headers['respuesta'] = False
			return resp
	else:
		resp = Response(status=401)
		resp.headers['respuesta'] = False
		return resp

#Verifica el login y si es correcto, le genera un token
@app.route('/auth', methods=['POST'])
def authorize():
	#Verifica el login y sie
	if login(request.form['nia'], request.form['password']).headers['respuesta'] == 'True':
		persona = Persona.search(request.form['nia'])[0]
		payload = {'NIA': request.form['nia'],
					'Nombre':persona.nombre,
					'Apellidos': persona.apellido1 + " " + persona.apellido2,
					'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
		token = jwt.encode(payload, app.config['SECRET'], algorithm='HS256')
		resp = Response(status=200)
		resp.headers['Token'] = token
		return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

#Verifica token pasado por header de http
@app.route('/auth', methods=['GET'])
def check():
	r = ['','']
	if request.headers.get('Authorization') != None:
		r = request.headers.get('Authorization').split()
	if r[0] != 'Bearer':
		resp = Response(status=401)
		resp.headers['respuesta'] = False
		return resp
	else:
		token = r[1]
		try:
			jwt.decode(token, app.config['SECRET'], algorithms='HS256')
			resp = Response(status=200)
			resp.headers['respuesta'] = 'True'
			return resp
		except Exception as e:
			resp = Response(status=401)
			resp.headers['respuesta'] = False
			return resp

#Comprueba si existe el usuario
@app.route('/login', methods=['POST'])
def login(nia=None, password=None):
	ldap = LdapApi(app.config['LDAP_URI'], request.form['nia'], request.form['password'])
	if ldap.auth() == 0:
		if Persona.search(request.form['nia']).count() > 0:
			resp = Response(status=200)
			resp.headers['respuesta'] = 'True'
			return resp
		else:
			resp = Response(status=401)
			resp.headers['respuesta'] = False
			return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

@app.route('/permisos/<int:nia>/<int:app_id>', methods=['GET'])
def getPermisos(nia, app_id):
	if check().headers['respuesta'] == 'True':
		try:
			persona_id = Persona.search(nia)[0].id
			permiso = Persona.getPermisos(app_id, persona_id)[0].rol
			resp = Response(status=200)
			resp.headers['respuesta'] = permiso
			return resp
		except Exception as e:
			resp = Response(status=200)
			resp.headers['respuesta'] = 0
			return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

@app.route('/delegado/<int:nia>', methods=['GET'])
def getDelegado(nia):
	if check().headers['respuesta'] == 'True':
		try:
			persona_id = Persona.search(nia)[0].id
			isDel = Persona.isDelegado(persona_id)[0]
			resp = Response(status=200)
			resp.headers['respuesta'] = True
			return resp
		except Exception as e:
			resp = Response(status=200)
			resp.headers['respuesta'] = False
			return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

@app.route('/delegadoTit/<int:nia>', methods=['GET'])
def isTitulacion(nia):
	if check().headers['respuesta'] == 'True':
		try:
			persona_id = Persona.search(nia)[0].id
			isDel = Persona.isDelegadoTitulacion(persona_id)[0]
			resp = Response(status=200)
			resp.headers['respuesta'] = True
			return resp
		except Exception as e:
			resp = Response(status=200)
			resp.headers['respuesta'] = False
			return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

@app.route('/delegadoCen/<int:nia>', methods=['GET'])
def isCentro(nia):
	if check().headers['respuesta'] == 'True':
		try:
			persona_id = Persona.search(nia)[0].id
			cargo = Persona.isDelegadoCentro(persona_id)[0].cargo
			resp = Response(status=200)
			resp.headers['respuesta'] = cargo
			return resp
		except Exception as e:
			resp = Response(status=200)
			resp.headers['respuesta'] = False
			return resp
	else:
		resp = Response(status=400)
		resp.headers['respuesta'] = False
		return resp

if __name__ == '__main__':
	app.run()
