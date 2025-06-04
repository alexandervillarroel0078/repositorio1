from models import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=True)  # Mejor con unique
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'), nullable=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=True)

    rol = db.relationship('Rol', backref='usuarios')
    profesor = db.relationship('Profesor', backref='usuario', uselist=False)
    alumno = db.relationship('Alumno', backref='usuario', uselist=False)

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"
