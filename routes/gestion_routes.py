from flask import Blueprint
from controllers import gestion_controller  # Importamos el controlador

gestion_bp = Blueprint('gestion_bp', __name__, url_prefix='/api/gestiones')

#http://127.0.0.1:5000/api/gestiones
@gestion_bp.route('/', methods=['GET'])
def listar_gestiones():
    return gestion_controller.listar_gestiones()


