from models import db
from sqlalchemy.orm import validates

class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)     # Requiere validación de texto
    apellido = db.Column(db.String(100), nullable=False)   # Requiere validación de texto
    carnet = db.Column(db.String(20), unique=True, nullable=True)

    # Validaciones adicionales opcionales
    @validates('nombre', 'apellido')
    def validate_nombre_apellido(self, key, value):
        if not value or not value.strip():
            raise ValueError(f'El campo "{key}" no puede estar vacío')
        if len(value) > 100:
            raise ValueError(f'El campo "{key}" no puede tener más de 100 caracteres')
        return value.strip().title()  # Estiliza: "juan perez" → "Juan Perez"
