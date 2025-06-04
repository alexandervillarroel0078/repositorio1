# Archivo: routes/predicciones_route.py
from flask import jsonify
from flask import Blueprint, request
from controllers.predicciones_controller import (
    hacer_prediccion_y_guardar,
    generar_predicciones_para_todos,
    listar_todas_las_predicciones,
    predicciones_por_alumno,
    generar_predicciones_por_grado_periodo,
    obtener_predicciones_por_materia,
    listar_materias_del_profesor
 
)

predicciones_bp = Blueprint('predicciones', __name__)

@predicciones_bp.route('/api/consulta-prediccion', methods=['POST'])
def predecir():
    data = request.get_json()
    return hacer_prediccion_y_guardar(
        alumno_id=data['alumno_id'],
        materia_id=data['materia_id'],
        periodo_id=data['periodo_id'],
        nota_parcial=data['nota_parcial'],
        asistencia=data['asistencia'],
        participacion=data['participacion']
    )

@predicciones_bp.route('/api/predicciones/generar', methods=['POST'])
def generar_para_todos():
    data = request.get_json()
    return generar_predicciones_para_todos(
        grado_id=data['grado_id'],
        materia_id=data['materia_id'],
        periodo_id=data['periodo_id']
    )


# @predicciones_bp.route('/api/predicciones/generar-multiples', methods=['POST'])
# def generar_multiples_materias():
#     data = request.get_json()
#     return generar_predicciones_por_profesor_grado_periodo(
#         profesor_id=data['profesor_id'],
#         grado_id=data['grado_id'],
#         periodo_id=data['periodo_id']
#     )

@predicciones_bp.route('/api/predicciones/generar-multiples', methods=['POST'])
def generar_multiples_materias():
    data = request.get_json()
    return generar_predicciones_por_grado_periodo(
        grado_id=data['grado_id'],
        periodo_id=data['periodo_id']
    )

@predicciones_bp.route('/api/predicciones', methods=['GET'])
def listar_predicciones():
    return listar_todas_las_predicciones()

@predicciones_bp.route('/api/predicciones/alumno/<int:alumno_id>', methods=['GET'])
def predicciones_alumno(alumno_id):
    return predicciones_por_alumno(alumno_id)



@predicciones_bp.route('/api/predicciones/grados/<int:profesor_id>', methods=['GET'])
def grados_del_profesor(profesor_id):
    from models.materia_profesor import MateriaProfesor
    from models.grado import Grado

    # Obtener todos los grados únicos donde el profesor tiene materias
    materia_grados = MateriaProfesor.query.filter_by(profesor_id=profesor_id).all()
    grado_ids = list(set(mg.grado_id for mg in materia_grados))
    
    grados = Grado.query.filter(Grado.id.in_(grado_ids)).all()

    resultado = [{'id': g.id, 'nombre': g.nombre} for g in grados]
    return jsonify(resultado)
















@predicciones_bp.route('/api/predicciones/listar-por-materia', methods=['GET'])
def listar_predicciones_por_materia():
    return obtener_predicciones_por_materia()


@predicciones_bp.route('/api/profesor/<int:profesor_id>/materias-prediccion', methods=['GET'])
def listar_materias_del_profesor_grado(profesor_id):
    return listar_materias_del_profesor(profesor_id)