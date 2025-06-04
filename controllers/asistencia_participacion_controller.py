import requests
from flask import request, jsonify,Blueprint
from datetime import date
from models import db
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion
from models.alumno_grado import AlumnoGrado
from models.periodo import Periodo
from models.grado import Grado
from models.gestion import Gestion
from models.nivel import Nivel
from models.materia import Materia
from models.nota_trimestre import NotaTrimestre

from controllers.profesor_controller import obtener_asistencias_por_grado
from controllers.profesor_controller import obtener_participaciones_por_materia_por_grado


def registrar_asistencia_participacion():
    data = request.get_json()

    alumno_id = data.get('alumno_id')
    grado_id = data.get('grado_id')
    periodo_id = data.get('periodo_id')
    tipo = data.get('tipo')  # 'asistencia' o 'participacion'
    valor = data.get('valor')
    fecha = data.get('fecha', date.today())  # usa hoy si no se manda fecha
    materia_id = data.get('materia_id')  # obligatoria en ciertos casos
    observaciones = data.get('observaciones', '')

    # 1. Validar alumno activo en grado
    alumno_grado = AlumnoGrado.query.filter_by(
        alumno_id=alumno_id,
        grado_id=grado_id,
        estado='en curso'
    ).first()
    if not alumno_grado:
        return jsonify({'error': 'El alumno no está inscrito activamente en ese grado.'}), 400

    # 2. Validar grado y gestión activa
    grado = Grado.query.get(grado_id)
    if not grado or not grado.gestion or grado.gestion.estado != 'activa':
        return jsonify({'error': 'El grado no pertenece a una gestión activa.'}), 400

    # 3. Validar periodo y su relación con la gestión del grado
    periodo = Periodo.query.get(periodo_id)
    if not periodo or periodo.gestion_id != grado.gestion_id:
        return jsonify({'error': 'El periodo no pertenece a la misma gestión del grado.'}), 400

    # 4. Obtener nombre del nivel (primaria/secundaria)
    nivel_nombre = grado.nivel.nombre.lower()

    # 5. Preparar filtro para verificar duplicado
    filtro_base = [
        HistorialAsistenciaParticipacion.alumno_id == alumno_id,
        HistorialAsistenciaParticipacion.grado_id == grado_id,
        HistorialAsistenciaParticipacion.periodo_id == periodo_id,
        HistorialAsistenciaParticipacion.tipo == tipo,
        HistorialAsistenciaParticipacion.fecha == fecha
    ]

    if tipo == 'participacion':
        # Participación siempre requiere materia (en primaria y secundaria)
        if not materia_id:
            return jsonify({'error': 'Materia es obligatoria para participación.'}), 400
        filtro_base.append(HistorialAsistenciaParticipacion.materia_id == materia_id)
        duplicado = HistorialAsistenciaParticipacion.query.filter(*filtro_base).first()

    elif tipo == 'asistencia':
        if nivel_nombre == 'primaria':
            # Asistencia por día y grado (sin materia)
            duplicado = HistorialAsistenciaParticipacion.query.filter(*filtro_base).first()
        elif nivel_nombre == 'secundaria':
            # Asistencia en secundaria requiere materia
            if not materia_id:
                return jsonify({'error': 'Materia es obligatoria para asistencia en secundaria.'}), 400
            filtro_base.append(HistorialAsistenciaParticipacion.materia_id == materia_id)
            duplicado = HistorialAsistenciaParticipacion.query.filter(*filtro_base).first()
        else:
            return jsonify({'error': 'Nivel no reconocido (debe ser Primaria o Secundaria).'}), 400

    else:
        return jsonify({'error': 'Tipo no reconocido. Debe ser "asistencia" o "participacion".'}), 400

    # 6. Verificar duplicado
    if duplicado:
        return jsonify({'error': 'Ya existe un registro para esta combinación de alumno, fecha y tipo.'}), 409

    # 7. Crear nuevo registro
    nuevo_registro = HistorialAsistenciaParticipacion(
        alumno_id=alumno_id,
        grado_id=grado_id,
        periodo_id=periodo_id,
        tipo=tipo,
        valor=valor,
        fecha=fecha,
        materia_id=materia_id if tipo == 'participacion' or nivel_nombre == 'secundaria' else None,
        observaciones=observaciones
    )

    db.session.add(nuevo_registro)
    db.session.commit()

    return jsonify({'mensaje': 'Registro guardado exitosamente.'}), 201


def registrar_asistencia_masiva():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Se espera una lista de asistencias'}), 400

    errores = []
    registros = []

    for index, item in enumerate(data):
        alumno_id = item.get('alumno_id')
        grado_id = item.get('grado_id')
        periodo_id = item.get('periodo_id')
        valor = item.get('valor')
        fecha = item.get('fecha', date.today())
        observaciones = item.get('observaciones', '')

        # Validaciones básicas por cada alumno
        alumno_grado = AlumnoGrado.query.filter_by(
            alumno_id=alumno_id,
            grado_id=grado_id,
            estado='en curso'
        ).first()

        grado = Grado.query.get(grado_id)
        periodo = Periodo.query.get(periodo_id)

        if not alumno_grado:
            errores.append(f"Alumno {alumno_id} no está inscrito en grado {grado_id}")
            continue
        if not grado or not grado.gestion or grado.gestion.estado != 'activa':
            errores.append(f"Grado {grado_id} no está en gestión activa")
            continue
        if not periodo or periodo.gestion_id != grado.gestion_id:
            errores.append(f"Periodo {periodo_id} no coincide con la gestión del grado")
            continue

        # Evitar duplicado de asistencia en primaria (por alumno y fecha)
        duplicado = HistorialAsistenciaParticipacion.query.filter_by(
            alumno_id=alumno_id,
            grado_id=grado_id,
            periodo_id=periodo_id,
            tipo='asistencia',
            fecha=fecha
        ).first()

        if duplicado:
            errores.append(f"Asistencia ya registrada para alumno {alumno_id} en fecha {fecha}")
            continue

        registro = HistorialAsistenciaParticipacion(
            alumno_id=alumno_id,
            grado_id=grado_id,
            periodo_id=periodo_id,
            tipo='asistencia',
            valor=valor,
            fecha=fecha,
            materia_id=None,
            observaciones=observaciones
        )
        registros.append(registro)

    if errores:
        return jsonify({'errores': errores}), 400

    for r in registros:
        db.session.add(r)
    db.session.commit()

    return jsonify({'mensaje': f'Se registraron {len(registros)} asistencias correctamente.'}), 201


def obtener_periodos_gestion_activa():
    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay una gestión activa'}), 404

    periodos = Periodo.query.filter_by(gestion_id=gestion_activa.id).order_by(Periodo.fecha_inicio).all()

    resultado = [{
        'id': p.id,
        'nombre': p.nombre,
        'fecha_inicio': p.fecha_inicio.strftime('%Y-%m-%d') if p.fecha_inicio else None,
        'fecha_fin': p.fecha_fin.strftime('%Y-%m-%d') if p.fecha_fin else None
    } for p in periodos]

    return jsonify(resultado), 200


def registrar_nota_parcial():
    datos = request.json  # lista de dicts
    for data in datos:
        nota = NotaTrimestre.query.filter_by(
            alumno_id=data['alumno_id'],
            materia_id=data['materia_id'],
            grado_id=data['grado_id'],
            periodo_id=data['periodo_id']
        ).first()

        if nota:
            nota.nota_parcial = data['nota_parcial']
        else:
            nota = NotaTrimestre(**data)
            db.session.add(nota)

    db.session.commit()
    return jsonify({"mensaje": "✅ Notas parciales registradas correctamente"})





