from . import db
from .gestion import Gestion

class PonderacionEvaluacion(db.Model):
    __tablename__ = 'ponderaciones_evaluacion'

    id = db.Column(db.Integer, primary_key=True)

    gestion_id = db.Column(db.Integer, db.ForeignKey('gestion.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Ej: "trimestre" o "anual"

    peso_nota_parcial = db.Column(db.Float, nullable=False)
    peso_asistencia = db.Column(db.Float, nullable=False)
    peso_participacion = db.Column(db.Float, nullable=False)

    gestion = db.relationship('Gestion', backref='ponderaciones')
