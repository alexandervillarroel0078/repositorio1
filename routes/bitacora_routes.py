from flask import Blueprint
from controllers import bitacora_controller

bitacora_bp = Blueprint('bitacora_bp', __name__)

@bitacora_bp.route('/api/bitacoras', methods=['GET'])
def listar_bitacoras():
    return bitacora_controller.listar_bitacoras()

@bitacora_bp.route('/api/bitacoras/<int:id>', methods=['GET'])
def obtener_bitacora(id):
    return bitacora_controller.obtener_bitacora(id)
