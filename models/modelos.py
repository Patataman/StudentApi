from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, TEXT

db = SQLAlchemy()

#Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),


class Persona(db.Model):
	__tablename__ = 'personas'

	id = db.Column(db.Integer, primary_key=True)
	nia = db.Column(db.Integer)
	nombre = db.Column(db.String(200))
	apellido1 = db.Column(db.String(200))
	apellido2 = db.Column(db.String(200))
	curso = db.Column(db.Integer)
	id_titulacion = db.Column(db.Integer)
	id_centro = db.Column(db.Integer)

	def __init__(self, nia, nombre, apellido1, apellido2, curso, id_titulacion):
		self.nia = nia
		self.nombre = nombre
		self.apellido1 = apellido1
		self.apellido2 = apellido2
		self.curso = curso
		self.id_titulacion = id_titulacion

	def __repr__(self):
		return 'id: {}, NIA: {}, Nombre: {}, Apellidos: {} {}, Curso: {}, Titulacion {}'.format(self.id, self.nia, self.nombre, self.apellido1, self.apellido2, self.curso, self.id_titulacion)

	@classmethod
	def search(self, nia):
		return db.session.query(Persona).filter_by(nia = nia)

	@classmethod
	def getPermisos(self, app_id, id):
		return db.session.query(Permisos).filter_by(id = id, app_id = app_id)

	@classmethod
	def isDelegado(self, id):
		return db.session.query(DelCurso).filter_by(id = id)

	@classmethod
	def isDelegadoTitulacion(self, id):
		return db.session.query(DelTitulacion).filter_by(id = id)

	@classmethod
	def isDelegadoCentro(self, id):
		return db.session.query(DelCentro).filter_by(id = id)

class Permisos(db.Model):
	__tablename__ = 'permisos'

	def __repr__(self):
		return 'id: {}, app_id: {}, rol: {}'.format(self.id, self.app_id, self.rol)

	id = db.Column(db.Integer, ForeignKey("Persona.id"), primary_key=True)
	app_id = db.Column(db.Integer, primary_key=True)
	rol = db.Column(db.Integer)

class DelCurso(db.Model):
	__tablename__ = 'delegadoscurso'

	def __repr__(self):
		return 'id: {}'.format(self.id)

	id = db.Column(db.Integer, ForeignKey("Persona.id"), primary_key=True)

class DelTitulacion(db.Model):
	__tablename__ = 'delegadostitulacion'

	def __repr__(self):
		return 'id: {}'.format(self.id)

	id = db.Column(db.Integer, ForeignKey("Persona.id"), primary_key=True)

class DelCentro(db.Model):
	__tablename__ = 'delegadoscentro'

	def __repr__(self):
		return 'id: {}, cargo: {}'.format(self.id, self.cargo)

	id = db.Column(db.Integer, ForeignKey("Persona.id"), primary_key=True)
	cargo = db.Column(db.Integer)

#	def __init__(self, id, app, rol):
#		self.id = id
#		self.app_id = app_id
#		self.rol = rol
#
#	@classmethod
#	def getPermisos(self, nia, app_id):
#		id = db.session.query(Persona).filter_by(nia = nia)[0].id
#		return db.session.query(Permisos).filter_by(id=id, app_id=app_id)[0].rol
#
#class DelCurso(db.Model):
#	__tablename__ = 'permisos'
#
#	id = db.Column(db.Integer, primary_key=True)
#	app_id = db.Column(db.Integer, primary_key=True)
#	rol = db.Column(db.Integer)
#
#	def __init__(self, id, app, rol):
#		self.id = id
#		self.app_id = app_id
#		self.rol = rol
#
#	@classmethod
#	def getPermisos(self, nia, app_id):
#		id = db.session.query(Persona).filter_by(nia = nia)[0].id
#		return db.session.query(Permisos).filter_by(id=id, app_id=app_id)[0].rol