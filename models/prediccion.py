from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models import db 

class Prediccion(db.Model):
    __tablename__ = 'prediccion'
    id = db.Column(db.Integer, primary_key=True)
    
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id'), nullable=False)
    
    nota_parcial = Column(Float, nullable=False)
    asistencia = Column(Float, nullable=False)
    participacion = Column(Float, nullable=False)

    rendimiento_predicho = Column(Float, nullable=False)
    clasificacion = Column(db.String(20), nullable=False)

    fecha_prediccion = Column(DateTime, default=datetime.utcnow)

    alumno = relationship("Alumno", backref="predicciones")
    materia = relationship("Materia", backref="predicciones")
    periodo = relationship("Periodo", backref="predicciones")