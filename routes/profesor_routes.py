#route/profesor_routes.py
from flask import Blueprint, request
from controllers import profesor_controller

profesor_bp = Blueprint('profesor_bp', __name__, url_prefix='/api')

#http://localhost:5000/api/profesores
@profesor_bp.route('/profesores', methods=['GET'])
def listar_profesores():
    return profesor_controller.listar_profesores()

#http://localhost:5000/api/profesores/1
@profesor_bp.route('/profesores/<int:id>', methods=['GET'])
def obtener_profesor(id):
    return profesor_controller.ver_profesor(id)

#http://localhost:5000/api/profesores/1/materias
@profesor_bp.route('/profesores/<int:id>/materias', methods=['GET'])
def materias_asignadas(id):
    return profesor_controller.materias_asignadas_profesor(id)

#http://localhost:5000/api/profesores/1/materias/1/estudiantes
@profesor_bp.route('/profesores/<int:profesor_id>/materias/<int:materia_id>/estudiantes', methods=['GET'])
def listar_estudiantes_por_materia(profesor_id, materia_id):
    return profesor_controller.obtener_estudiantes_por_materia(profesor_id, materia_id)

# http://localhost:5000/api/asistencias/por-grado?grado_id=16&profesor_id=4&nivel=1
@profesor_bp.route('/asistencias/por-grado')
def obtener_asistencias_por_grado():
    return profesor_controller.obtener_asistencias_por_grado()

# http://localhost:5000/api/participaciones/por-materia-grado?grado_id=16&profesor_id=4&nivel_id=1&materia_id=1
@profesor_bp.route('/participaciones/por-materia-grado')
def obtener_participaciones_por_materia_por_grado():
    return profesor_controller.obtener_participaciones_por_materia_por_grado()

#http://localhost:5000/api/notas/por-materia-grado?grado_id=16&profesor_id=4&nivel_id=1&materia_id=1
@profesor_bp.route('/notas/por-materia-grado')
def obtener_notas_por_materia_por_grado():
    return profesor_controller.obtener_notas_por_materia_por_grado()












#http://localhost:5000/api/notas-trimestre/asistencia?grado_id=16&nivel=1&profesor_id=4&materia_id=1&periodo_id=10
@profesor_bp.route('/notas-trimestre/asistencia', methods=['PUT'])
def registrar_asistencia_trimestre():
    return profesor_controller.registrar_asistencia_en_nota_trimestre()

#http://localhost:5000/api/notas-trimestre/participaciones?grado_id=16&nivel_id=1&profesor_id=4&materia_id=1&periodo_id=10
@profesor_bp.route('/notas-trimestre/participaciones', methods=['PUT'])
def obtener_y_registrar_participaciones_por_materia_por_grado():
    return profesor_controller.obtener_y_registrar_participaciones_por_materia_por_grado()






















