from flask import Blueprint, request
from controllers import rol_controller

rol_bp = Blueprint('rol_bp', __name__)
#http://localhost:5000/api/roles
@rol_bp.route('/api/roles', methods=['GET'])
def listar_roles():
    return rol_controller.listar_roles()
#http://localhost:5000/api/roles/1
@rol_bp.route('/api/roles/<int:id>', methods=['GET'])
def ver_rol(id):
    return rol_controller.ver_rol(id)

@rol_bp.route('/api/roles', methods=['POST'])
def crear_rol():
    return rol_controller.crear_rol(request)

@rol_bp.route('/api/roles/<int:id>', methods=['PUT'])
def editar_rol(id):
    return rol_controller.editar_rol(id, request)

@rol_bp.route('/api/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    return rol_controller.eliminar_rol(id)
