from flask import Blueprint, request
from controllers import global_controller  # Importamos el controlador

# Crear un blueprint para las rutas de historial
historial_bp = Blueprint('historial_bp', __name__)

# Ruta para listar todos los registros de historial
@historial_bp.route('/api/historial', methods=['GET'])
def listar_historial():
    return global_controller.listar_historial()

# Ruta para filtrar los registros de historial por múltiples parámetros
@historial_bp.route('/api/historial/filtrar', methods=['GET'])
def filtrar_historial():
    return global_controller.filtrar_historial()

