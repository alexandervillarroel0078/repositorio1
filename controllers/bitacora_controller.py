from flask import jsonify
from models import db
from models.bitacora import Bitacora

def listar_bitacoras():
    bitacoras = Bitacora.query.order_by(Bitacora.fecha_hora.desc()).all()
    return jsonify([
        {
            "id": b.id,
            "usuario_id": b.usuario_id,
            "usuario_nombre": b.usuario.nombre_completo if b.usuario else None,
            "accion": b.accion,
            "descripcion": b.descripcion,
            "fecha_hora": b.fecha_hora.isoformat() if b.fecha_hora else None
        } for b in bitacoras
    ])

def obtener_bitacora(id):
    b = Bitacora.query.get_or_404(id)
    return jsonify({
        "id": b.id,
        "usuario_id": b.usuario_id,
        "usuario_nombre": b.usuario.nombre_completo if b.usuario else None,
        "accion": b.accion,
        "descripcion": b.descripcion,
        "fecha_hora": b.fecha_hora.isoformat() if b.fecha_hora else None
    })
