from flask import Blueprint, request
from controllers import periodo_controller

periodo_bp = Blueprint('periodo_bp', __name__)

@periodo_bp.route('/api/periodos', methods=['GET'])
def listar_periodos():
    return periodo_controller.listar_periodos()

@periodo_bp.route('/api/periodos/<int:id>', methods=['GET'])
def ver_periodo(id):
    return periodo_controller.ver_periodo(id)

@periodo_bp.route('/api/periodos', methods=['POST'])
def crear_periodo():
    return periodo_controller.crear_periodo(request)

@periodo_bp.route('/api/periodos/<int:id>', methods=['PUT'])
def editar_periodo(id):
    return periodo_controller.editar_periodo(id, request)

@periodo_bp.route('/api/periodos/<int:id>', methods=['DELETE'])
def eliminar_periodo(id):
    return periodo_controller.eliminar_periodo(id)
