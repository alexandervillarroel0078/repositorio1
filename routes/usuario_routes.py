from flask import Blueprint, request
from controllers import usuario_controller
from controllers.usuario_controller import cambiar_password

usuario_bp = Blueprint('usuario_bp', __name__)

#http://localhost:5000/api/usuarios
@usuario_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    return usuario_controller.listar_usuarios()

#http://localhost:5000/api/crear-alumnoss 
@usuario_bp.route('/api/crear-alumnoss', methods=['POST'])
def crear_alumno():
    return usuario_controller.crear_alumno()

#   "nombre": "Juanita",
#   "apellido": "Pérez Villarroel"

#http://localhost:5000/api/inscripciones
@usuario_bp.route('/api/inscripciones', methods=['POST'])
def inscribir_alumno():
    return usuario_controller.inscribir_alumno()

#   "alumno_id": 6
#http://localhost:5000/api/cambiar-password
@usuario_bp.route('/api/cambiar-password', methods=['PUT'])
def ruta_cambiar_password():
    return cambiar_password()
#"nueva_contraseña": "miNuevaClaveSegura"