from flask import jsonify
from models import db
from models.rol import Rol
from traits.bitacora_trait import registrar_bitacora

def listar_roles():
    roles = Rol.query.all()
    return jsonify([
        {
            "id": r.id,
            "nombre": r.nombre,
            "descripcion": r.descripcion
        } for r in roles
    ])

def ver_rol(id):
    r = Rol.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "nombre": r.nombre,
        "descripcion": r.descripcion
    })

def crear_rol(request):
    data = request.get_json()
    nuevo = Rol(
        nombre = data['nombre'],
        descripcion = data.get('descripcion')
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora("rol", f"creó rol ID {nuevo.id}")
    return jsonify({"mensaje": "Rol creado correctamente", "id": nuevo.id})

def editar_rol(id, request):
    r = Rol.query.get_or_404(id)
    data = request.get_json()
    r.nombre = data['nombre']
    r.descripcion = data.get('descripcion')
    db.session.commit()
    registrar_bitacora("rol", f"editó rol ID {r.id}")
    return jsonify({"mensaje": "Rol actualizado correctamente"})

def eliminar_rol(id):
    r = Rol.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    registrar_bitacora("rol", f"eliminó rol ID {id}")
    return jsonify({"mensaje": "Rol eliminado correctamente"})
