from flask import Blueprint, jsonify, g
from utils.token import token_requerido  # Ya lo tienes en utils/token.py

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil', methods=['GET'])
@token_requerido
def perfil():
    return jsonify({
        "mensaje": "Bienvenido",
        "usuario": g.usuario
    })
