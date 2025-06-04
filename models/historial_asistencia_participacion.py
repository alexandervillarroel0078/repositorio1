from models import db
from sqlalchemy.orm import validates

class HistorialAsistenciaParticipacion(db.Model):
    __tablename__ = 'historial_asistencia_participacion'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=True)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id'), nullable=False)

    tipo = db.Column(db.String(20), nullable=False)  # 'asistencia' o 'participacion'
    valor = db.Column(db.Float, nullable=False)      # Ej: nota de 1 a 100
    fecha = db.Column(db.Date, nullable=True)       # Día de registro

    observaciones = db.Column(db.Text, nullable=True)

    alumno = db.relationship('Alumno', backref='asistencias_participaciones')
    materia = db.relationship('Materia', backref='asistencias_participaciones')
    grado = db.relationship('Grado', backref='asistencias_participaciones')
    periodo = db.relationship('Periodo', backref='asistencias_participaciones')

    __table_args__ = (
        db.CheckConstraint("tipo IN ('asistencia', 'participacion')", name='check_tipo_valido'),
        db.CheckConstraint("valor >= 0 AND valor <= 100", name='check_valor_rango'),
    )

    @validates('tipo')
    def validate_tipo(self, key, value):
        if value not in ['asistencia', 'participacion']:
            raise ValueError("Tipo debe ser 'asistencia' o 'participacion'")
        return value

    @validates('valor')
    def validate_valor(self, key, value):
        if not (0 <= value <= 100):
            raise ValueError("Valor debe estar entre 0 y 100")
        return value

    def __repr__(self):
        return f"<HistorialAsistenciaParticipacion id={self.id} alumno_id={self.alumno_id} tipo={self.tipo}>"
