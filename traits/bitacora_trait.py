# traits/bitacora_trait.py
from flask import request
from models import db, Bitacora

def obtener_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def registrar_bitacora(tabla, accion, usuario_id=None):
    ip = obtener_ip()
    entrada = Bitacora(
        usuario_id=usuario_id,
        accion=accion,
        tabla=tabla,
        ip=ip
    )
    db.session.add(entrada)
    db.session.commit()
