# models/gestion.py

from . import db
from sqlalchemy.orm import validates

class Gestion(db.Model):
    __tablename__ = 'gestion'

    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False, unique=True)  # Ej: 2025
    estado = db.Column(db.String(20), default='activa')  # activa, finalizada, futura
    descripcion = db.Column(db.String(100))  # Ej: "Gestión Escolar 2025"

    def __repr__(self):
        return f'<Gestion {self.anio}>'

    @validates('anio')
    def validate_anio(self, key, value):
        if value < 2000 or value > 2100:
            raise ValueError('El año debe estar entre 2000 y 2100')
        return value

    @validates('estado')
    def validate_estado(self, key, value):
        estados_validos = ['activa', 'finalizada', 'en_proceso']
        if value not in estados_validos:
            raise ValueError(f'El estado debe ser uno de: {", ".join(estados_validos)}')
        return value
