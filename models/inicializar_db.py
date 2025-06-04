from . import db

def inicializar_db():
    print("📦 Modelos detectados:", db.metadata.tables.keys())  # línea clave
    db.create_all()
