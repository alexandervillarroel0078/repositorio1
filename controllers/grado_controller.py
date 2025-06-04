from models import db
from flask import request, jsonify
from models import Grado, Gestion


def listar_grados_agrupados_por_gestion():
    try:
        gestiones = Gestion.query.order_by(Gestion.anio).all()

        resultado = []
        for gestion in gestiones:
            grados = []
            for grado in gestion.grados:
                grados.append({
                    'grado_id': grado.id,
                    'nombre_grado': grado.nombre,
                    'descripcion_grado': grado.descripcion,
                })
            resultado.append({
                'gestion_id': gestion.id,
                'gestion_estado': gestion.estado,
                'nombre_gestion': gestion.anio,
                'descripcion_gestion': gestion.descripcion,
                'grados': grados
            })

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def obtener_materias_por_grado(gestion_id, grado_id):
    grado = Grado.query.filter_by(id=grado_id, gestion_id=gestion_id).first()

    if not grado:
        return jsonify({'error': 'Grado no encontrado para esa gestión'}), 404

    materias = [
        {
            'materia_id': mg.materia.id,
            'nombre': mg.materia.nombre,
            'descripcion': mg.materia.descripcion
        }
        for mg in grado.materias_asignadas
    ]

    return jsonify({
        'gestion': grado.gestion.anio,
        'grado': grado.nombre,
        'materias': materias
    })




