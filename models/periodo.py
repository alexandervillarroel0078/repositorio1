from . import db

class Periodo(db.Model):
    __tablename__ = 'periodos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)  # Ej: "1er Bimestre"
    
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)

    gestion_id = db.Column(db.Integer, db.ForeignKey('gestion.id'), nullable=False)
    gestion = db.relationship('Gestion', backref='periodos')

    __table_args__ = (
        db.UniqueConstraint('nombre', 'gestion_id', name='uq_nombre_periodo_gestion'),
    )

    def __repr__(self):
        return f"<Periodo {self.nombre} - Gestion {self.gestion_id}>"
