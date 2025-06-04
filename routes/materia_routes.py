from flask import Blueprint, request
from controllers import materia_controller

materia_bp = Blueprint('materia_bp', __name__)
# http://localhost:5000/api/materias
@materia_bp.route('/api/materias', methods=['GET'])
def listar_materias():
    return materia_controller.listar_materias()

# http://localhost:5000/api/materias/1 
@materia_bp.route('/api/materias/<int:id>', methods=['GET'])
def ver_materia(id):
    return materia_controller.ver_materia(id)

# http://localhost:5000/api/materias
@materia_bp.route('/api/materias', methods=['POST'])
def crear_materia():
    return materia_controller.crear_materia(request)

# http://localhost:5000/api/materias/1
@materia_bp.route('/api/materias/<int:id>', methods=['PUT'])
def editar_materia(id):
    return materia_controller.editar_materia(id, request)

# http://localhost:5000/api/materias/1 
@materia_bp.route('/api/materias/<int:id>', methods=['DELETE'])
def eliminar_materia(id):
    return materia_controller.eliminar_materia(id)

# http://localhost:5000/api/materias/1/estudiantes
@materia_bp.route('/api/materias/<int:materia_id>/estudiantes', methods=['GET'])
def listar_alumnos_por_materia(materia_id):
    return materia_controller.listar_alumnos_por_materia(materia_id)

#http://127.0.0.1:5000/api/asistencias/alumno?alumno_id=5&gestion=2&materia_id=1&periodo_id=2
@materia_bp.route('/api/asistencias/alumno', methods=['GET'])
def obtener_asistencias_de_alumno():
    return materia_controller.obtener_asistencias_de_alumno()
