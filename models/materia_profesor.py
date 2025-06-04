from models import db

class MateriaProfesor(db.Model):
    __tablename__ = 'materia_profesor'
    id = db.Column(db.Integer, primary_key=True)

    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)

    profesor = db.relationship('Profesor', backref='materias_asignadas')
    materia = db.relationship('Materia', backref='profesores_asignados')
    grado = db.relationship('Grado', backref='materias_grado')

    __table_args__ = (
        db.UniqueConstraint('profesor_id', 'materia_id', 'grado_id', name='uq_profesor_materia_grado'),
    )
