from models import db

class MateriaGrado(db.Model):
    __tablename__ = 'materia_grado'

    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)

    materia = db.relationship('Materia', backref='materia_grados')
    grado = db.relationship('Grado', backref='materias_asignadas')
     


    __table_args__ = (
        db.UniqueConstraint('materia_id', 'grado_id', name='uq_materia_grado'),
    )
