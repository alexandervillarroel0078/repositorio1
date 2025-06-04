from models import db
from sqlalchemy.orm import validates

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)  # Evita duplicados
    descripcion = db.Column(db.String(255), nullable=True)

    nivel_id = db.Column(db.Integer, db.ForeignKey('niveles.id'), nullable=False)  # Relación obligatoria
    nivel = db.relationship('Nivel', backref='materias')

    @validates('nombre')
    def validate_nombre(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre de la materia no puede estar vacío.")
        if len(value.strip()) < 3:
            raise ValueError("El nombre de la materia debe tener al menos 3 caracteres.")
        return value.strip().title()  # Normaliza el formato, ej: "Lenguaje"
