# routes/historial_asistencia_route.py

from flask import Blueprint
from controllers import asistencia_participacion_controller

historial_asistencia_bp = Blueprint('historial_asistencia_bp', __name__)


#http://localhost:5000/api/registrar-asistencia-presentacion
@historial_asistencia_bp.route('/api/registrar-asistencia-presentacion', methods=['POST'])
def crear_historial():
    return asistencia_participacion_controller.registrar_asistencia_participacion()


#http://localhost:5000/api/asistencia/masiva                                                              
@historial_asistencia_bp.route('/api/asistencia/masiva', methods=['POST'])
def crear_asistencia_masiva():
    return asistencia_participacion_controller.registrar_asistencia_masiva()

#http://localhost:5000/api/periodos/activos
@historial_asistencia_bp.route('/api/periodos/activos', methods=['GET'])
def obtener_periodos():
    return asistencia_participacion_controller.obtener_periodos_gestion_activa()

#http://localhost:5000/api/notas-trimestre/registrar-parcial
@historial_asistencia_bp.route('/api/notas-trimestre/registrar-parcial', methods=['POST'])
def registrar_nota_parcial():
    return asistencia_participacion_controller.registrar_nota_parcial()

