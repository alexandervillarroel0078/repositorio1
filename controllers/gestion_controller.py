from flask import Blueprint, jsonify
from models.gestion import Gestion
from models import db

gestion_bp = Blueprint('gestion_bp', __name__)

def listar_gestiones():
    gestiones = Gestion.query.order_by(Gestion.anio.desc()).all()
    resultado = [
        {
            'id': g.id,
            'anio': g.anio,
            'estado': g.estado,
            'descripcion': g.descripcion
        } for g in gestiones
    ]
    return jsonify(resultado), 200
 