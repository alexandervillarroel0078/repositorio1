from flask import request, jsonify
from models.alumno import Alumno
from models.alumno_grado import AlumnoGrado
from models.grado import Grado
from models.gestion import Gestion
from models.materia_grado import MateriaGrado
from models.materia import Materia
from models.nota_trimestre import NotaTrimestre
from models.ponderaciones_evaluacion import PonderacionEvaluacion
from models.periodo import Periodo
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion

#funciona
def listar_alumnos():
    alumnos = Alumno.query.all()

    lista_alumnos = [
        {
            'id': alumno.id,
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'Ci': alumno.carnet,
        }
        for alumno in alumnos
    ]

    return jsonify(lista_alumnos), 200

#funciona
def ver_alumno(id):
    alumno = Alumno.query.get(id)
    
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    return jsonify({
        'id': alumno.id,
        'nombre': alumno.nombre,
        'apellido': alumno.apellido
    }), 200

#funciona
def obtener_perfil_alumno(id):
    alumno = Alumno.query.get(id)

    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    perfil = {
        'id': alumno.id,
        'nombre': alumno.nombre,
        'apellido': alumno.apellido,
        'Ci': alumno.carnet,
        # Aquí puedes agregar más datos si lo deseas
    }

    return jsonify(perfil), 200

#funciona
def obtener_materias_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)

    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = []

    for inscripcion in alumno.historial_grados:
        grado = inscripcion.grado
        gestion = grado.gestion

        materias = Materia.query\
            .join(MateriaGrado)\
            .filter(MateriaGrado.grado_id == grado.id)\
            .all()

        materias_list = [
            {
                'id': m.id,
                'nombre': m.nombre,
                'descripcion': m.descripcion
            } for m in materias
        ]

        resultado.append({
            'gestion': gestion.anio,
            'grado': grado.nombre,
            'estado': inscripcion.estado,
            'materias': materias_list
        })

    return jsonify({
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'materias_por_gestion': resultado
    }), 200

#funciona
def obtener_asistencias_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = {
        "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
        "asistencias": {}
    }

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno.id).all()

    for nota in notas:
        if nota.asistencia_trimestre is None:
            continue  # ignorar si no hay asistencia registrada

        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre

        if gestion_anio not in resultado["asistencias"]:
            resultado["asistencias"][gestion_anio] = {
                "estado": estado,
                "grados": {}
            }

        grados = resultado["asistencias"][gestion_anio]["grados"]

        if grado_nombre not in grados:
            # Obtener el estado de aprobación del grado desde AlumnoGrado
            alumno_grado = AlumnoGrado.query.filter_by(
                alumno_id=alumno.id,
                grado_id=nota.grado.id
            ).first()
            estado_aprobacion = alumno_grado.estado if alumno_grado else "desconocido"

            grados[grado_nombre] = {
                "estado_aprobacion": estado_aprobacion,
                "periodos": {}
            }

        periodos = grados[grado_nombre]["periodos"]

        if periodo_nombre not in periodos:
            periodos[periodo_nombre] = {}

        if materia_nombre not in periodos[periodo_nombre]:
            periodos[periodo_nombre][materia_nombre] = []

        periodos[periodo_nombre][materia_nombre].append({
            "observaciones": "Extraído de nota trimestral",
            "valor": nota.asistencia_trimestre
        })

    return jsonify(resultado), 200

#funciona
def obtener_participacion_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = {
        "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
        "participaciones": {}
    }

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno.id).all()

    for nota in notas:
        if nota.participacion_trimestre is None:
            continue  # ignorar si no hay participación registrada

        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre

        if gestion_anio not in resultado["participaciones"]:
            resultado["participaciones"][gestion_anio] = {
                "estado": estado,
                "grados": {}
            }

        grados = resultado["participaciones"][gestion_anio]["grados"]

        # Si es la primera vez que se encuentra este grado
        if grado_nombre not in grados:
            # Obtener el estado de aprobación del alumno en ese grado
            relacion = AlumnoGrado.query.filter_by(
                alumno_id=alumno.id,
                grado_id=nota.grado.id
            ).first()
            estado_aprobacion = relacion.estado if relacion else "desconocido"

            # Inicializar estructura del grado
            grados[grado_nombre] = {
                "estado_aprobacion": estado_aprobacion,
                "periodos": {}
            }

        periodos = grados[grado_nombre]["periodos"]

        if periodo_nombre not in periodos:
            periodos[periodo_nombre] = {}

        if materia_nombre not in periodos[periodo_nombre]:
            periodos[periodo_nombre][materia_nombre] = []

        periodos[periodo_nombre][materia_nombre].append({
            "observaciones": "Extraído de nota trimestral",
            "valor": nota.participacion_trimestre
        })

    return jsonify(resultado), 200

#funiona
def obtener_notas_alumno():
    alumno_id = request.args.get('alumno_id')
    if not alumno_id:
        return jsonify({'error': 'Parámetro alumno_id es requerido'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno_id).all()

    resultado = {
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'notas': {}
    }

    for nota in notas:
        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre
        valor = nota.nota_parcial

        # Inicializar gestión
        if gestion_anio not in resultado['notas']:
            resultado['notas'][gestion_anio] = {
                'estado': estado,
                'grados': {}
            }

        grados = resultado['notas'][gestion_anio]['grados']

        # Inicializar grado con estado_aprobacion
        if grado_nombre not in grados:
            # Buscar el estado_aprobacion desde AlumnoGrado
            relacion = AlumnoGrado.query.filter_by(
                alumno_id=alumno.id,
                grado_id=nota.grado_id
            ).first()
            estado_aprobacion = relacion.estado if relacion else "desconocido"

            grados[grado_nombre] = {
                'estado_aprobacion': estado_aprobacion,
                'periodos': {}
            }

        periodos = grados[grado_nombre]['periodos']

        # Inicializar periodo
        if periodo_nombre not in periodos:
            periodos[periodo_nombre] = {}

        # Inicializar materia
        if materia_nombre not in periodos[periodo_nombre]:
            periodos[periodo_nombre][materia_nombre] = []

        # Agregar nota
        periodos[periodo_nombre][materia_nombre].append({
            'observaciones': 'Nota parcial',
            'valor': valor
        })

    return jsonify(resultado), 200

#funiona
def obtener_historial_academico():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    historial = []

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno_id).all()

    # Agrupar por (gestion_id, grado_id, materia_id)
    agrupado = {}
    for nota in notas:
        key = (nota.grado.gestion.id, nota.grado.id, nota.materia.id)
        if key not in agrupado:
            agrupado[key] = {
                'notas': [],
                'grado': nota.grado,
                'materia': nota.materia,
                'gestion': nota.grado.gestion
            }
        agrupado[key]['notas'].append(nota)

    for (gestion_id, grado_id, materia_id), grupo in agrupado.items():
        notas_trimestre = grupo['notas']
        gestion = grupo['gestion']
        grado = grupo['grado']
        materia = grupo['materia']

        # Saltar gestiones que no están finalizadas
        if gestion.estado != 'finalizada':
            continue

        # Verificar que el alumno tenga estado aprobado en ese grado
        alumno_grado = AlumnoGrado.query.filter_by(
            alumno_id=alumno_id,
            grado_id=grado.id
        ).first()

        if not alumno_grado or alumno_grado.estado != 'aprobado':
            continue

        # Obtener ponderación para esa gestión
        ponderacion = PonderacionEvaluacion.query.filter_by(
            gestion_id=gestion_id,
            tipo='trimestre'
        ).first()

        if not ponderacion:
            continue  # Podrías registrar un log aquí si es necesario

        # Calcular promedio ponderado del año
        total = 0
        for nota in notas_trimestre:
            parcial = nota.nota_parcial or 0
            asistencia = nota.asistencia_trimestre or 0
            participacion = nota.participacion_trimestre or 0

            final_trimestre = (
                parcial * ponderacion.peso_nota_parcial +
                asistencia * ponderacion.peso_asistencia +
                participacion * ponderacion.peso_participacion
            )
            total += final_trimestre

        nota_final = round(total / len(notas_trimestre), 2) if notas_trimestre else 0
        estado = "Aprobado" if nota_final >= 51 else "Reprobado"

        historial.append({
            'gestion': gestion.anio,
            'grado': grado.nombre,
            'materia': materia.nombre,
            'nota_final': nota_final,
            'estado': estado
        })

    return jsonify({
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'historial': sorted(historial, key=lambda x: (x['gestion'], x['grado']))
    }), 200

#funiona
def obtener_promedios_por_grado():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno_id).all()

    agrupado = {}
    for nota in notas:
        gestion = nota.grado.gestion
        if gestion.estado != 'finalizada':
            continue

        alumno_grado = AlumnoGrado.query.filter_by(
            alumno_id=alumno_id,
            grado_id=nota.grado.id
        ).first()

        if not alumno_grado or alumno_grado.estado != 'aprobado':
            continue

        key = (gestion.id, nota.grado.id)
        if key not in agrupado:
            agrupado[key] = {
                'gestion': gestion.anio,
                'grado': nota.grado.nombre,
                'notas_finales': [],
                'ponderacion': PonderacionEvaluacion.query.filter_by(
                    gestion_id=gestion.id, tipo='trimestre'
                ).first()
            }

        parcial = nota.nota_parcial or 0
        asistencia = nota.asistencia_trimestre or 0
        participacion = nota.participacion_trimestre or 0
        pond = agrupado[key]['ponderacion']

        if pond:
            final_trimestre = (
                parcial * pond.peso_nota_parcial +
                asistencia * pond.peso_asistencia +
                participacion * pond.peso_participacion
            )
            agrupado[key]['notas_finales'].append(final_trimestre)

    promedios = []
    for (gestion_id, grado_id), data in agrupado.items():
        notas = data['notas_finales']
        promedio = round(sum(notas) / len(notas), 2) if notas else 0
        estado = "Aprobado" if promedio >= 51 else "Reprobado"
        promedios.append({
            'gestion': data['gestion'],
            'grado': data['grado'],
            'promedio': promedio,
            'estado': estado
        })

    return jsonify({
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'promedios_por_grado': sorted(promedios, key=lambda x: (x['gestion'], x['grado']))
    }), 200