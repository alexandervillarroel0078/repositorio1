from flask import Blueprint
from controllers import grado_controller

grado_bp = Blueprint('grado_bp', __name__, url_prefix='/api/grados')

#http://localhost:5000/api/grados/agrupados
@grado_bp.route('/agrupados', methods=['GET'])
def grados_agrupados():
    return grado_controller.listar_grados_agrupados_por_gestion()

# http://localhost:5000/api/grados/gestion/1/grado/1/materias
@grado_bp.route('/gestion/<int:gestion_id>/grado/<int:grado_id>/materias', methods=['GET'])
def ver_materias_por_grado(gestion_id, grado_id):
    return grado_controller.obtener_materias_por_grado(gestion_id, grado_id)
