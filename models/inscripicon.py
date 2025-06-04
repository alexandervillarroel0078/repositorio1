# models/inscripcion.py
from models import db
from datetime import datetime

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    gestion_id = db.Column(db.Integer, db.ForeignKey('gestion.id'), nullable=False)
    fecha_inscripcion = db.Column(db.Date, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activa')  # activa, retirada, etc.

    alumno = db.relationship('Alumno', backref='inscripciones')
    gestion = db.relationship('Gestion', backref='inscripciones')
