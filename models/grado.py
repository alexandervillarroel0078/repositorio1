from models import db
from sqlalchemy.orm import validates

class Grado(db.Model):
    __tablename__ = 'grados'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)  # Ej: "1ro A", "2do B"
    descripcion = db.Column(db.String(100), nullable=True)

    gestion_id = db.Column(db.Integer, db.ForeignKey('gestion.id'), nullable=False)
    gestion = db.relationship('Gestion', backref='grados')
    nivel_id = db.Column(db.Integer, db.ForeignKey('niveles.id'), nullable=False)

    nivel = db.relationship('Nivel', backref='grados')
    @validates('nombre')
    def validate_nombre(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre del grado no puede estar vacío.")
        return value.strip().upper()  # Ej: "1RO A"

    @validates('descripcion')
    def validate_descripcion(self, key, value):
        return value.strip().capitalize() if value else None
