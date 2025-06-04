from models import db
from models.alumno import Alumno
from models.materia import Materia
from models.periodo import Periodo
from models.grado import Grado 


class NotaTrimestre(db.Model):
    __tablename__ = 'nota_trimestre'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id'), nullable=False)

    nota_parcial = db.Column(db.Float)  # Solo esta se registra manualmente

    asistencia_trimestre = db.Column(db.Float)           # Se calcula automáticamente (1-100)
    participacion_trimestre = db.Column(db.Float)        # Se calcula automáticamente (1-100)

    alumno = db.relationship('Alumno', backref='notas_bimestre')
    materia = db.relationship('Materia', backref='notas_bimestre')
    grado = db.relationship('Grado', backref='notas_bimestre')
    periodo = db.relationship('Periodo', backref='notas_bimestre')
