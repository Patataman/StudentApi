from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import JSON, TEXT

db = SQLAlchemy()

class Persona(db.Model):
	__tablename__ = 'personas'

	id = db.Column(db.Integer, primary_key=True)
	nia = db.Column(db.Integer)
	nombre = db.Column(db.String(200))
	apellido1 = db.Column(db.String(200))
	apellido2 = db.Column(db.String(200))
	curso = db.Column(db.Integer)
	id_titulacion = db.Column(db.Integer)

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