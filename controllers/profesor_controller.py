# /controllers/profesor_controller.py
from flask import Blueprint, jsonify, request
from models import db
from models.profesor import Profesor
from models.materia_profesor import MateriaProfesor
from models.gestion import Gestion
from models.alumno_grado import AlumnoGrado
from models.alumno import Alumno
from models.grado import Grado
from models.periodo import Periodo
from models.nivel import Nivel
from models.nota_trimestre import NotaTrimestre
from models.materia import Materia
from sqlalchemy.orm import joinedload
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion
from models.ponderaciones_evaluacion import PonderacionEvaluacion
from sqlalchemy import func, case

profesor_bp = Blueprint('profesor_bp', __name__)

#funciona
def listar_profesores():
    profesores = Profesor.query.filter_by(estado='activo').order_by(Profesor.id.asc()).all()
    resultado = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'estado': p.estado,
            'Ci': p.carnet,
        } for p in profesores
    ]
    return jsonify(resultado), 200

#funciona
def ver_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404

    resultado = {
        'id': profesor.id,
        'nombre': profesor.nombre,
        'apellido': profesor.apellido,
        'estado': profesor.estado,
        'Ci': profesor.carnet,
    }
    return jsonify(resultado), 200

#funciona
def materias_asignadas_profesor(profesor_id):
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404

    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    asignaciones = MateriaProfesor.query \
        .filter_by(profesor_id=profesor_id) \
        .join(MateriaProfesor.grado) \
        .filter(Grado.gestion_id == gestion_activa.id) \
        .join(MateriaProfesor.materia) \
        .join(Grado.nivel) \
        .all()

    materias = []
    for asignacion in asignaciones:
        materias.append({
            'materia_id': asignacion.materia.id,
            'materia': asignacion.materia.nombre,
            'grado_id': asignacion.grado.id, 
            'grado': asignacion.grado.nombre,
            'nivel_id': asignacion.grado.nivel.id,
            'nivel': asignacion.grado.nivel.nombre,
            'gestion': gestion_activa.anio
        })

    resultado = {
        'profesor': {
            'id': profesor.id,
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'estado': profesor.estado
        },
        'materias_asignadas': materias
    }

    return jsonify(resultado), 200

#funciona
def obtener_estudiantes_por_materia(profesor_id, materia_id):
    # Buscar gestión activa
    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    # Buscar asignaciones de esa materia en la gestión activa Y del profesor indicado
    asignaciones = MateriaProfesor.query \
        .join(Grado) \
        .filter(MateriaProfesor.materia_id == materia_id) \
        .filter(MateriaProfesor.profesor_id == profesor_id) \
        .filter(Grado.gestion_id == gestion_activa.id) \
        .all()

    if not asignaciones:
        return jsonify({'error': 'No se encontró la materia asignada al profesor en esta gestión'}), 404

    estudiantes = []
    total = 0

    profesor = asignaciones[0].profesor
    materia = asignaciones[0].materia

    for asignacion in asignaciones:
        alumnos_grado = AlumnoGrado.query \
            .filter_by(grado_id=asignacion.grado_id, estado='en curso') \
            .join(Alumno) \
            .all()

        for ag in alumnos_grado:
            estudiantes.append({
                'id': ag.alumno.id,
                'nombre': ag.alumno.nombre,
                'apellido': ag.alumno.apellido,
                'estado': ag.estado,
                'grado': asignacion.grado.nombre
            })
            total += 1

    return jsonify({
        'materia_id': materia.id,
        'materia': materia.nombre,
        'gestion': gestion_activa.anio,
        'profesor_id': profesor.id,
        'profesor': f'{profesor.nombre} {profesor.apellido}',
        'total_alumnos': total,
        'estudiantes': estudiantes
    }), 200

#funciona
def obtener_asistencias_por_grado():
    grado_id = request.args.get('grado_id', type=int)
    profesor_id = request.args.get('profesor_id', type=int)
    nivel_id = request.args.get('nivel', type=int)

    if not grado_id or not profesor_id or not nivel_id:
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    profesor = Profesor.query.get(profesor_id)
    grado = Grado.query.get(grado_id)

    if not profesor or not grado:
        return jsonify({'error': 'Datos no encontrados'}), 404

    gestion = grado.gestion
    nivel = grado.nivel

    periodos = Periodo.query.filter_by(gestion_id=gestion.id).all()
    periodos_data = []

    for periodo in periodos:
        query = HistorialAsistenciaParticipacion.query.filter_by(
            grado_id=grado_id,
            periodo_id=periodo.id,
            tipo='asistencia'
        )

        if nivel_id == 1:  # Primaria
            registros = query.join(Alumno, Alumno.id == HistorialAsistenciaParticipacion.alumno_id)\
                .with_entities(
                    HistorialAsistenciaParticipacion.alumno_id,
                    Alumno.nombre,
                    Alumno.apellido,
                    HistorialAsistenciaParticipacion.valor
                ).all()

            datos = {}
            for r in registros:
                if r.alumno_id not in datos:
                    datos[r.alumno_id] = {
                        'alumno_id': r.alumno_id,
                        'nombre': r.nombre,
                        'apellido': r.apellido,
                        'nombre_completo': f"{r.nombre} {r.apellido}",
                        'asistencias_completas': 0,
                        'llegadas_tarde': 0,
                        'muy_tarde': 0,
                        'ausencias': 0,
                        'licencias': 0,
                        'valores_validos': []
                    }

                if r.valor == 100:
                    datos[r.alumno_id]['asistencias_completas'] += 1
                    datos[r.alumno_id]['valores_validos'].append(100)
                elif r.valor == 80:
                    datos[r.alumno_id]['llegadas_tarde'] += 1
                    datos[r.alumno_id]['valores_validos'].append(80)
                elif r.valor == 50:
                    datos[r.alumno_id]['muy_tarde'] += 1
                    datos[r.alumno_id]['valores_validos'].append(50)
                elif r.valor == 1:
                    datos[r.alumno_id]['ausencias'] += 1
                    datos[r.alumno_id]['valores_validos'].append(1)
                elif r.valor == 0:
                    datos[r.alumno_id]['licencias'] += 1

            data = []
            for alumno in datos.values():
                promedio = round(sum(alumno['valores_validos']) / len(alumno['valores_validos']), 2) if alumno['valores_validos'] else 0
                alumno['promedio_asistencia'] = promedio
                alumno['total_clases'] = len(alumno['valores_validos']) + alumno['licencias']
                data.append(alumno)

        else:  # Secundaria
            materias_docente = MateriaProfesor.query.filter_by(
                profesor_id=profesor_id,
                grado_id=grado_id
            ).with_entities(MateriaProfesor.materia_id).all()

            materias_ids = [m.materia_id for m in materias_docente]

            if not materias_ids:
                data = []
            else:
                registros = query.filter(HistorialAsistenciaParticipacion.materia_id.in_(materias_ids))\
                    .join(Alumno, Alumno.id == HistorialAsistenciaParticipacion.alumno_id)\
                    .with_entities(
                        HistorialAsistenciaParticipacion.alumno_id,
                        Alumno.nombre,
                        Alumno.apellido,
                        HistorialAsistenciaParticipacion.materia_id,
                        HistorialAsistenciaParticipacion.valor
                    ).all()

                datos = {}
                for r in registros:
                    key = (r.alumno_id, r.materia_id)
                    if key not in datos:
                        datos[key] = {
                            'alumno_id': r.alumno_id,
                            'materia_id': r.materia_id,
                            'nombre': r.nombre,
                            'apellido': r.apellido,
                            'nombre_completo': f"{r.nombre} {r.apellido}",
                            'asistencias_completas': 0,
                            'llegadas_tarde': 0,
                            'muy_tarde': 0,
                            'ausencias': 0,
                            'licencias': 0,
                            'valores_validos': []
                        }

                    if r.valor == 100:
                        datos[key]['asistencias_completas'] += 1
                        datos[key]['valores_validos'].append(100)
                    elif r.valor == 80:
                        datos[key]['llegadas_tarde'] += 1
                        datos[key]['valores_validos'].append(80)
                    elif r.valor == 50:
                        datos[key]['muy_tarde'] += 1
                        datos[key]['valores_validos'].append(50)
                    elif r.valor == 1:
                        datos[key]['ausencias'] += 1
                        datos[key]['valores_validos'].append(1)
                    elif r.valor == 0:
                        datos[key]['licencias'] += 1

                data = []
                for alumno in datos.values():
                    promedio = round(sum(alumno['valores_validos']) / len(alumno['valores_validos']), 2) if alumno['valores_validos'] else 0
                    alumno['promedio_asistencia'] = promedio
                    alumno['total_clases'] = len(alumno['valores_validos']) + alumno['licencias']
                    data.append(alumno)

        periodos_data.append({
            'periodo_id': periodo.id,
            'nombre': periodo.nombre,
            'asistencias': data
        })

    return jsonify({
        'docente': {
            'id': profesor.id,
            'nombre': f'{profesor.nombre} {profesor.apellido}'
        },
        'grado': {
            'id': grado.id,
            'nombre': grado.nombre
        },
        'nivel': nivel.nombre,
        'gestion': gestion.anio,
        'periodos': periodos_data
    }), 200

#funciona
def obtener_participaciones_por_materia_por_grado():
    profesor_id = request.args.get('profesor_id', type=int)
    grado_id = request.args.get('grado_id', type=int)
    nivel_id = request.args.get('nivel_id', type=int)
    materia_id = request.args.get('materia_id', type=int)

    if not (profesor_id and grado_id and nivel_id and materia_id):
        return jsonify({'error': 'Faltan parámetros: profesor_id, grado_id, nivel_id o materia_id'}), 400

    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    periodos = Periodo.query.filter_by(gestion_id=gestion_activa.id).order_by(Periodo.id).all()
    if not periodos:
        return jsonify({'error': 'No hay periodos registrados en esta gestión'}), 404

    grado = Grado.query.get(grado_id)
    nivel = Nivel.query.get(nivel_id)
    materia = Materia.query.get(materia_id)

    if not grado or not nivel or not materia:
        return jsonify({'error': 'Grado, nivel o materia no encontrados'}), 404

    resultados = []
    TOTAL_ESPERADAS = 10

    alumnos = db.session.query(Alumno).join(AlumnoGrado).filter(
        AlumnoGrado.grado_id == grado_id
    ).all()

    for periodo in periodos:
        participaciones_alumnos = []

        for alumno in alumnos:
            participaciones = HistorialAsistenciaParticipacion.query.filter_by(
                tipo='participacion',
                grado_id=grado_id,
                periodo_id=periodo.id,
                alumno_id=alumno.id,
                materia_id=materia_id
            ).all()

            total_esperadas = len(participaciones)
            suma_valores = sum([p.valor for p in participaciones])

            if total_esperadas == 0:
                continue

            nota = round((suma_valores / (100 * TOTAL_ESPERADAS)) * 100, 2)
            no_participo = TOTAL_ESPERADAS - total_esperadas

            participaciones_alumnos.append({
                'alumno_id': alumno.id,
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'participaciones_registradas': total_esperadas,
                'total_esperadas': TOTAL_ESPERADAS,
                'no_participo': no_participo,
                'suma_valores': suma_valores,
                'nota_participacion': nota
            })

        resultados.append({
            'periodo_id': periodo.id,
            'periodo': periodo.nombre,
            'participaciones': participaciones_alumnos
        })

    return jsonify({
        'profesor_id': profesor_id,
        'grado_id': grado_id,
        'materia_id': materia_id,
        'nombre_grado': grado.nombre,
        'nivel_id': nivel_id,
        'nombre_nivel': nivel.nombre,
        'materia': {
            'id': materia.id,
            'nombre': materia.nombre
        },
        'gestion': gestion_activa.anio,
        'participaciones_por_periodo': resultados
    })


#funciona
def obtener_notas_por_materia_por_grado():
    grado_id = request.args.get('grado_id', type=int)
    profesor_id = request.args.get('profesor_id', type=int)
    nivel_id = request.args.get('nivel_id', type=int)
    materia_id = request.args.get('materia_id', type=int)

    if not grado_id or not profesor_id or not nivel_id or not materia_id:
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    gestion = Gestion.query.filter_by(estado='activa').first()
    if not gestion:
        return jsonify({'error': 'No hay gestión activa'}), 404

    materia_asignada = MateriaProfesor.query \
        .join(MateriaProfesor.materia) \
        .filter(
            MateriaProfesor.profesor_id == profesor_id,
            MateriaProfesor.grado_id == grado_id,
            MateriaProfesor.materia_id == materia_id,
            Materia.nivel_id == nivel_id
        ).first()

    if not materia_asignada:
        return jsonify({'error': 'Materia no asignada al profesor en este grado y nivel'}), 404

    materia = materia_asignada.materia
    profesor = materia_asignada.profesor
    grado = materia_asignada.grado

    ponderacion = PonderacionEvaluacion.query.filter_by(
        gestion_id=gestion.id, tipo='trimestre'
    ).first()

    if not ponderacion:
        return jsonify({'error': 'No hay ponderación definida para esta gestión'}), 400

    periodos = Periodo.query.filter_by(gestion_id=gestion.id).all()

    data = {
        "docente": {
            "id": profesor.id,
            "nombre": f"{profesor.nombre} {profesor.apellido}"
        },
        "materia": {
            "id": materia.id,
            "nombre": materia.nombre
        },
        "grado": {
            "id": grado.id,
            "nombre": grado.nombre
        },
        "nivel": grado.nivel.nombre,
        "gestion": gestion.anio,
        "periodos": []
    }

    for periodo in periodos:
        notas = NotaTrimestre.query.options(joinedload(NotaTrimestre.alumno)) \
            .filter_by(
                grado_id=grado_id,
                materia_id=materia_id,
                periodo_id=periodo.id
            ).all()

        notas_data = []
        for n in notas:
            nota_parcial = n.nota_parcial or 0
            asistencia = n.asistencia_trimestre or 0
            participacion = n.participacion_trimestre or 0

            nota_sin_ponderar = round(nota_parcial + asistencia + participacion, 2)

            aporte_parcial = nota_parcial * ponderacion.peso_nota_parcial
            aporte_asistencia = asistencia * ponderacion.peso_asistencia
            aporte_participacion = participacion * ponderacion.peso_participacion

            nota_ponderada = round(aporte_parcial + aporte_asistencia + aporte_participacion, 2)

            notas_data.append({
                "alumno_id": n.alumno.id,
                "nombre": n.alumno.nombre,
                "apellido": n.alumno.apellido,
                "nota_parcial": n.nota_parcial,
                "asistencia_trimestre": n.asistencia_trimestre,
                "participacion_trimestre": n.participacion_trimestre,
                "nota_final_sin_ponderacion": nota_sin_ponderar,
                "nota_final_con_ponderacion": nota_ponderada,
                "aporte_parcial_ponderda": round(aporte_parcial, 2),
                "aporte_asistencia_ponderda": round(aporte_asistencia, 2),
                "aporte_participacion_ponderda": round(aporte_participacion, 2)
            })

        data["periodos"].append({
            "periodo_id": periodo.id,
            "nombre": periodo.nombre,
            "notas": notas_data
        })

    return jsonify(data), 200




#funciona
def registrar_asistencia_en_nota_trimestre():
    grado_id = request.args.get('grado_id', type=int)
    profesor_id = request.args.get('profesor_id', type=int)
    nivel_id = request.args.get('nivel', type=int)
    materia_id = request.args.get('materia_id', type=int)
    periodo_id = request.args.get('periodo_id', type=int)

    if not grado_id or not profesor_id or not nivel_id or not materia_id or not periodo_id:
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    # Obtener datos ya calculados desde el mismo método de asistencias
    from controllers.profesor_controller import obtener_asistencias_por_grado

    response = obtener_asistencias_por_grado()
    if response[1] != 200:
        return jsonify({'error': 'No se pudo obtener asistencias'}), 500

    periodos = response[0].json.get('periodos', [])

    # Buscar el periodo específico
    periodo_data = next((p for p in periodos if p['periodo_id'] == periodo_id), None)
    if not periodo_data:
        return jsonify({'error': 'Periodo no encontrado en los datos de asistencia'}), 404

    asistencias = periodo_data.get('asistencias', [])
    afectados = []

    for alumno in asistencias:
        alumno_id = alumno['alumno_id']
        promedio_asistencia = alumno['promedio_asistencia']

        nota = NotaTrimestre.query.filter_by(
            alumno_id=alumno_id,
            materia_id=materia_id,
            grado_id=grado_id,
            periodo_id=periodo_id
        ).first()

        if nota:
            nota.asistencia_trimestre = promedio_asistencia
        else:
            nueva = NotaTrimestre(
                alumno_id=alumno_id,
                materia_id=materia_id,
                grado_id=grado_id,
                periodo_id=periodo_id,
                asistencia_trimestre=promedio_asistencia
            )
            db.session.add(nueva)

        afectados.append({
            'alumno_id': alumno_id,
            'asistencia': promedio_asistencia
        })

    db.session.commit()
    return jsonify({
        'mensaje': '✅ Asistencia registrada en nota_trimestre correctamente',
        'periodo_id': periodo_id,
        'materia_id': materia_id,
        'registros': afectados
    }), 200

#funciona
def obtener_y_registrar_participaciones_por_materia_por_grado():
    profesor_id = request.args.get('profesor_id', type=int)
    grado_id = request.args.get('grado_id', type=int)
    nivel_id = request.args.get('nivel_id', type=int)
    materia_id = request.args.get('materia_id', type=int)
    periodo_id = request.args.get('periodo_id', type=int)

    if not all([profesor_id, grado_id, nivel_id, materia_id, periodo_id]):
        return jsonify({'error': 'Faltan parámetros: profesor_id, grado_id, nivel_id, materia_id o periodo_id'}), 400

    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    periodo = Periodo.query.filter_by(id=periodo_id, gestion_id=gestion_activa.id).first()
    if not periodo:
        return jsonify({'error': 'Periodo no encontrado en la gestión activa'}), 404

    grado = Grado.query.get(grado_id)
    nivel = Nivel.query.get(nivel_id)
    materia = Materia.query.get(materia_id)

    if not grado or not nivel or not materia:
        return jsonify({'error': 'Grado, nivel o materia no encontrados'}), 404

    TOTAL_ESPERADAS = 10
    alumnos = db.session.query(Alumno).join(AlumnoGrado).filter(
        AlumnoGrado.grado_id == grado_id
    ).all()

    participaciones_alumnos = []

    for alumno in alumnos:
        participaciones = HistorialAsistenciaParticipacion.query.filter_by(
            tipo='participacion',
            grado_id=grado_id,
            periodo_id=periodo_id,
            alumno_id=alumno.id,
            materia_id=materia_id
        ).all()

        total_esperadas = len(participaciones)
        suma_valores = sum(p.valor for p in participaciones)

        if total_esperadas == 0:
            continue

        nota = round((suma_valores / (100 * TOTAL_ESPERADAS)) * 100, 2)

        # Actualizar o insertar en nota_trimestre
        nota_trimestre = NotaTrimestre.query.filter_by(
            alumno_id=alumno.id,
            grado_id=grado_id,
            periodo_id=periodo_id,
            materia_id=materia_id
        ).first()

        if nota_trimestre:
            nota_trimestre.participacion_trimestre = nota
        else:
            nueva = NotaTrimestre(
                alumno_id=alumno.id,
                grado_id=grado_id,
                periodo_id=periodo_id,
                materia_id=materia_id,
                participacion_trimestre=nota
            )
            db.session.add(nueva)

        participaciones_alumnos.append({
            'alumno_id': alumno.id,
            'nombre': alumno.nombre,
            'nota_participacion': nota
        })

    db.session.commit()

    return jsonify({
        'participaciones': participaciones_alumnos,
        'mensaje': '✅ Participaciones registradas correctamente en nota_trimestre'
    }), 200








