from models import db
from sqlalchemy.orm import validates

class Profesor(db.Model):
    __tablename__ = 'profesores'

    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False, default='activo')  # Valores: 'activo', 'inactivo'
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    carnet = db.Column(db.String(20), unique=True, nullable=False)

    @validates('nombre', 'apellido')
    def validate_nombre_apellido(self, key, value):
        if not value or not value.strip():
            raise ValueError(f'El campo "{key}" no puede estar vacío')
        if len(value.strip()) > 100:
            raise ValueError(f'El campo "{key}" no puede tener más de 100 caracteres')
        return value.strip().title()  # Estiliza: "carlos perez" → "Carlos Perez"
