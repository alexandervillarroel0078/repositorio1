from models import db
from datetime import datetime
from sqlalchemy.orm import validates

class Bitacora(db.Model):
    __tablename__ = 'bitacora'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    accion = db.Column(db.String(255), nullable=False)
    tabla = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='bitacoras')

    @validates('accion')
    def validate_accion(self, key, value):
        if not value or not value.strip():
            raise ValueError("La acción no puede estar vacía.")
        return value.strip()

    @validates('tabla')
    def validate_tabla(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre de la tabla no puede estar vacío.")
        return value.strip().lower()

    @validates('ip')
    def validate_ip(self, key, value):
        return value.strip() if value else None
