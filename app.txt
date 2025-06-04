from flask import Flask
from flask_cors import CORS
from models import db  # IMPORTANTE: importar db desde models/__init__.py
from flask_migrate import Migrate
from models.inicializar_db import inicializar_db
from routes.auth import auth_bp
from routes.perfil import perfil_bp


app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/aulainteligente'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_aula_inteligente'

db.init_app(app)  # Vincula db al app
migrate = Migrate(app, db)
CORS(app)

# Crea las tablas si no existen
with app.app_context():
    inicializar_db()

# Rutas
app.register_blueprint(auth_bp)
app.register_blueprint(perfil_bp)

@app.route('/')
def inicio():
    return '🎓 Aula Inteligente backend funcionando'

if __name__ == '__main__':
    app.run(debug=True)
