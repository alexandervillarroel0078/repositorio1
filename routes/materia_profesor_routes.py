from flask import Blueprint, request
from controllers import materia_profesor_controller

materia_profesor_bp = Blueprint('materia_profesor_bp', __name__)

@materia_profesor_bp.route('/api/materias-profesor', methods=['GET'])
def listar_materias_profesor():
    return materia_profesor_controller.listar_materias_profesor()

@materia_profesor_bp.route('/api/materias-profesor/<int:id>', methods=['GET'])
def ver_materia_profesor(id):
    return materia_profesor_controller.ver_materia_profesor(id)

@materia_profesor_bp.route('/api/materias-profesor', methods=['POST'])
def crear_materia_profesor():
    return materia_profesor_controller.crear_materia_profesor(request)

@materia_profesor_bp.route('/api/materias-profesor/<int:id>', methods=['PUT'])
def editar_materia_profesor(id):
    return materia_profesor_controller.editar_materia_profesor(id, request)

@materia_profesor_bp.route('/api/materias-profesor/<int:id>', methods=['DELETE'])
def eliminar_materia_profesor(id):
    return materia_profesor_controller.eliminar_materia_profesor(id)
