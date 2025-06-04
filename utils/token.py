from functools import wraps
from flask import request, jsonify, g, current_app
import jwt

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            if bearer.startswith('Bearer '):
                token = bearer.split(" ")[1]

        if not token:
            return jsonify({"mensaje": "Token requerido"}), 401

        try:
            datos = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            g.usuario = datos  # guardamos el usuario en 'g'
        except jwt.ExpiredSignatureError:
            return jsonify({"mensaje": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorador
