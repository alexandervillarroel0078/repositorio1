from models import db
from sqlalchemy.orm import validates

class Nivel(db.Model):
    __tablename__ = 'niveles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)  # Evita duplicados como 'Primaria'

    @validates('nombre')
    def validate_nombre(self, key, value):
        if not value.strip():
            raise ValueError("El nombre del nivel no puede estar vacío.")
        if len(value) < 3:
            raise ValueError("El nombre del nivel debe tener al menos 3 caracteres.")
        return value.title()  # Guarda como "Primaria", "Secundaria", etc.
