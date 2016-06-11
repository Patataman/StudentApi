# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from lib.ldapApi import LdapApi
from models.modelos import db, Persona

#jwt es la librería para el token.
import jwt, json, lib.Student as Student, datetime

app = Flask(__name__)
app.config.from_pyfile('lib/config.cfg')
db.app = app
db.init_app(app)


#─────────▄──────────────▄
#────────▌▒█───────────▄▀▒▌
#────────▌▒▒▀▄───────▄▀▒▒▒▐
#───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
#─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐        So much code
#───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌
#──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌
#──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
#─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌
#─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌    wow
#─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐
#▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌
#▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐
#─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
#─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
#──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌
#────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀         very REST API
#───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀                      wow
#──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀

'''
	! ATENCION !

	ESTA API SE AUTODESTRUIRÁ EN 5- es broma, xdddd

	Para poder usar esta API deberás ser miembro de 
	la Universidad Carlos III de Madrid y saber tu 
	NIA y contraseña.

	Con ella se podrá principalmente:
		- Buscar usuarios dados su nia o nombre.
		- Obtener un token de verificación si el NIA
		  y contraseña son correctos Y ADEMÁS perteneces
		  a la Delegación de Estudiantes.
		- Verificar el Token generado
		- Poder verificar si una persona (NIA + contraseña)
		  pertenece a la Delegación de Estudiantes.
		- Conocer si dado un NIA esa persona es: 
			+ Delegado de Curso
			+ Delegado de Titulación
			+ Delegado de Centro

'''



''' 
	Ruta base, permite verificar si la API está 
	levantada mediante el True que devuelve
'''
@app.route('/')
def index():
	return json.JSONEncoder().encode({"result": True})

''' /student/<int:nia> 
	Devuelve la información relacionada con el alumno
	del nia que se introduce.
	Concretamente devuelve:
		-Nombre
		-Correo
		-NIA
'''
@app.route('/student/<int:nia>', methods=['GET'])
def getByNia(nia):
	if json.loads(check())['result'] == True:
		students = None
		nia = '(uid=*' + str(nia) + '*)'
		try:
			students = Student.getStudent(nia)
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})

		#Parsear resultados y return como json
		if students != None:
			#Nunca debería llamarse, el nia es único
			if len(students)>1:
				parser = '['
				bol = 0
				for i in students:
					if bol != 0:
						parser += ','
					if bol == 0: bol = 1
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				return json.JSONEncoder().encode({"result": [parser]})
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				return json.JSONEncoder().encode({"result": [parser]})
		else:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})

''' /student/<string:name>
	Devuelve la información de todos los miembros
	de la universidad con el nombre introducido, 
	se dan dos situaciones:

	1- El número de resultados es muy grande (por ejemplo, 50)
		+ Devuelve un codigo 500 y False

	2- El número de resultados es lo suficientemente pequeño:
		+ Devuelve el array parseado en JSON con la información
		  de todos los alumnos encontrados.

	Ej: String = "Adrián" devolverá un 500
		String = "Adrián Alonso" puede devolver 
				 la información de 10 resultados
				 y un código 200.
	
'''
@app.route('/student/<string:name>', methods=['GET'])
def getByName(name):
	if json.loads(check())['result'] == True:
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
			return json.JSONEncoder().encode({"result": False})

		if len(nombre) == 2:
			result = '(cn=*' + nombre[0] + ' ' + nombre[1] + '*)'
		elif len(nombre) == 1:
			result = '(cn=*' + nombre[0] + '*)'

		students = None
		try:
			students = Student.getStudent(result)
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})

		#Parsear resultados y return como json
		if students != None:
			if len(students)>1:
				parser = '['
				bol = 0
				for i in students:
					if bol != 0:
						parser += ','
					if bol == 0: bol = 1
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				parser += ']'
				return json.JSONEncoder().encode({"result": [parser]})
			else:
				parser = ''
				for i in students:
					parser += json.dumps([i.name, i.uid, i.email], separators=(',',':'))
				return json.JSONEncoder().encode({"result": [parser]})
		else:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})


''' 
	/auth Method = POST

	Permite generar el token correspondiente para poder
	utilizar la aplicación.

	Para ello deberá pasarse el NIA y la contraseña correspondiente.
	Con el nia, nombre y contraseña genera un token que tiene una duración válida de 1h.

'''
#Verifica el login y si es correcto, le genera un token
@app.route('/auth', methods=['POST'])
def authorize():
	#Verifica el login y sie
	if json.loads(login(request.form['nia'], request.form['password']))['result'] == True:
		persona = Persona.search(request.form['nia'])[0]
		payload = {'NIA': request.form['nia'],
					'Nombre':persona.nombre,
					'Apellidos': persona.apellido1 + " " + persona.apellido2,
					'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
		token = jwt.encode(payload, app.config['SECRET'], algorithm='HS256')
		#resp.headers['Token'] = token
		return json.JSONEncoder().encode({"result": token})
	else:
		return json.JSONEncoder().encode({"result": False})


''' 
	/auth Method = GET

	Permite verificar si un token es válido.

	Para ello se debe pasar en la cabecera HTTP un apartado
	llamado 'Authorization', este campo debe tener el valor:

		Bearer <token>

	Si el token es correcto, devuelve un código 200 y True, si 
	es incorrecto se devuelve 401 y False.

'''
#Verifica token pasado por header de http
@app.route('/auth', methods=['GET'])
def check():
	r = ['','']
	if request.headers.get('Authorization') != None:
		r = request.headers.get('Authorization').split()
	if r[0] != 'Bearer':
		return json.JSONEncoder().encode({"result": False})
	else:
		token = r[1]
		try:
			jwt.decode(token, app.config['SECRET'], algorithms='HS256')
			return json.JSONEncoder().encode({"result": True})
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})

'''
	Permite verificar si la persona correspondiente pertenece
	a la tabla de Personas (Es decir, forma parte de alguna forma
	de la Delegacion)

	El método /auth (POST) lo utiliza para verificar 
	la identidad del usuario.

	Se puede utilizar sin necesidad del Token.

	Si todo funciona correctamente devuelve un código 200
	y True.

	Si la persona es miembro de la universidad pero no está
	en la tabla personas se devuelve un código 401 y False.
	Si ocurre algún error en el login se devuelve un 400 y False.

'''
#Comprueba si existe el usuario
@app.route('/login', methods=['POST'])
def login(nia=None, password=None):
	ldap = LdapApi(app.config['LDAP_URI'], request.form['nia'], request.form['password'])
	if ldap.auth() == 0:
		if Persona.search(request.form['nia']).count() > 0:
			return json.JSONEncoder().encode({"result": True})
		else:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})


'''
	/permisos/<int:nia>/<int:app_id>

	Permite obtener los permisos de un usuario (NIA)
	para cierta aplicación (app_id).

	Si la persona tiene permisos para esa aplicación se
	devuelve un código 200 y los permisos correspondientes.
	Si la persona no tiene permisos se devuelve un código 200,
	pero los permisos serán 0.

	Si ocurre algún error se devuelve un código 400 y False.
'''
@app.route('/permisos/<int:nia>/<int:app_id>', methods=['GET'])
def getPermisos(nia, app_id):
	if json.loads(check())['result'] == True:
		try:
			persona_id = Persona.search(nia)[0].id
			permiso = Persona.getPermisos(app_id, persona_id)[0].rol
			return json.JSONEncoder().encode({"result": [permiso]})
		except Exception as e:
			return json.JSONEncoder().encode({"result": [0]})
	else:
		return json.JSONEncoder().encode({"result": False})


'''
	/delegado/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a.
	Para ello se comprueba con la tabla delegadoscurso de la BBDD.

	Si es delegado se devuelve un 200 y True.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.
'''
@app.route('/delegado/<int:nia>', methods=['GET'])
def getDelegado(nia):
	if json.loads(check())['result'] == True:
		try:
			persona_id = Persona.search(nia)[0].id
			isDel = Persona.isDelegado(persona_id)[0]
			return json.JSONEncoder().encode({"result": True})
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})

'''
	/delegadoTit/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a de titulación.
	Para ello se comprueba con la tabla delegadostitulacion de la BBDD.

	Si es delegado se devuelve un 200 y True.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.
'''
@app.route('/delegadoTit/<int:nia>', methods=['GET'])
def isTitulacion(nia):
	if json.loads(check())['result'] == True:
		try:
			persona_id = Persona.search(nia)[0].id
			isDel = Persona.isDelegadoTitulacion(persona_id)[0]
			return json.JSONEncoder().encode({"result": True})
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})

'''
	/delegadoCen/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a de titulación.
	Para ello se comprueba con la tabla delegadoscentro de la BBDD.

	Si es delegado se devuelve un 200 y su cargo correspondiente.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.
'''
@app.route('/delegadoCen/<int:nia>', methods=['GET'])
def isCentro(nia):

	if json.loads(check())['result'] == True:
		try:
			persona_id = Persona.search(nia)[0].id
			cargo = Persona.isDelegadoCentro(persona_id)[0].cargo
			return json.JSONEncoder().encode({"result": [cargo]})
		except Exception as e:
			return json.JSONEncoder().encode({"result": False})
	else:
		return json.JSONEncoder().encode({"result": False})

if __name__ == '__main__':
	app.run()
