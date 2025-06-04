from flask import Blueprint, request
from controllers import alumno_controller

# Usamos url_prefix para evitar repetir /api/alumnos
alumno_bp = Blueprint('alumno_bp', __name__, url_prefix='/api/alumnos')

#CRUD
#http://127.0.0.1:5000/api/alumnos
@alumno_bp.route('/', methods=['GET'])
def listar_alumnos():
    return alumno_controller.listar_alumnos()

#http://127.0.0.1:5000/api/alumnos/1
@alumno_bp.route('/<int:id>', methods=['GET'])
def ver_alumno(id):
     return alumno_controller.ver_alumno(id)

#http://127.0.0.1:5000/api/alumnos/1/perfil
@alumno_bp.route('/<int:id>/perfil', methods=['GET'])
def ver_perfil_alumno(id):
    return alumno_controller.obtener_perfil_alumno(id)

#http://localhost:5000/api/alumnos/materias?alumno_id=1
@alumno_bp.route('/materias', methods=['GET'])
def materias_por_alumno():
    return alumno_controller.obtener_materias_por_alumno()

#http://localhost:5000/api/alumnos/asistencias?alumno_id=1
@alumno_bp.route('/asistencias', methods=['GET'])
def asistencias_por_alumno():
    return alumno_controller.obtener_asistencias_por_alumno();

# #http://localhost:5000/api/alumnos/participacion?alumno_id=1
@alumno_bp.route('/participacion', methods=['GET'])
def obtener_participacion_alumno():
    return alumno_controller.obtener_participacion_por_alumno()

# http://localhost:5000/api/alumnos/notas?alumno_id=1
@alumno_bp.route('/notas', methods=['GET'])
def obtener_notas_alumno():
     return alumno_controller.obtener_notas_alumno()

# http://localhost:5000/api/alumnos/historial-academico?alumno_id=1
@alumno_bp.route('/historial-academico', methods=['GET'])
def obtener_historial_academico():
     return alumno_controller.obtener_historial_academico()

# http://localhost:5000/api/alumnos/promedios-por-grado?alumno_id=1
@alumno_bp.route('/promedios-por-grado', methods=['GET'])
def promedios_por_grado():
    return alumno_controller.obtener_promedios_por_grado()
