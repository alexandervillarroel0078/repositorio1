# routes/auth.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from models.usuario import Usuario
from models.rol import Rol
import jwt
import datetime
from models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    if not correo or not password:
        return jsonify({"mensaje": "Usuario y contraseña requeridos"}), 400

    try:
        usuario = db.session.query(Usuario).join(Rol).filter(Usuario.correo == correo).add_columns(
            Usuario.id, Usuario.nombre_usuario, Usuario.password_hash, Usuario.correo, Rol.nombre.label('rol_nombre')
        ).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            payload = {
                'id': usuario.id,
                'nombre_usuario': usuario.nombre_usuario,
                'rol': usuario.rol_nombre,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
            }

            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'token': token,
                'usuario': {
                    'id': usuario.id,
                    'nombre_usuario': usuario.nombre_usuario,
                    'correo': usuario.correo,
                    'rol': usuario.rol_nombre
                }
            }), 200
        else:
            return jsonify({"mensaje": "Credenciales incorrectas"}), 401

    except Exception as e:
        return jsonify({"mensaje": "Error en el servidor", "error": str(e)}), 500
