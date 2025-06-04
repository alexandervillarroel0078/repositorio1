from models import db
from sqlalchemy import CheckConstraint

class AlumnoGrado(db.Model):
    __tablename__ = 'alumno_grado'

    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False, default='en curso')
    
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)

    alumno = db.relationship('Alumno', backref='historial_grados')
    grado = db.relationship('Grado', backref='alumnos_inscritos')

    # Restricciones y mejoras
    __table_args__ = (
    CheckConstraint(
        "estado IN ('pendiente', 'en curso', 'aprobado', 'no aprobado')",
        name='check_estado_valido'
    ),
    )

