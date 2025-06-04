from flask import jsonify, request
from models import db
from models.prediccion import Prediccion
from models.nota_trimestre import NotaTrimestre
from models.alumno import Alumno
from models.alumno_grado import AlumnoGrado
from models.materia_profesor import MateriaProfesor
from models.periodo import Periodo
from models.gestion import Gestion
from models.materia_grado import MateriaGrado
from models.materia import Materia
import numpy as np
import joblib

# modelo = joblib.load('modelo_lineal.pkl')
import os
PESOS = (0.6, 0.2, 0.2) 
ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'modelo_lineal.pkl')
modelo = joblib.load(ruta_modelo)

def clasificar_rendimiento(valor):
    if valor < 60:
        return "Bajo"
    elif valor < 80:
        return "Medio"
    else:
        return "Alto"



# def generar_predicciones_por_profesor_grado_periodo(profesor_id, grado_id, periodo_id):
#     materias_asignadas = MateriaProfesor.query.filter_by(
#         profesor_id=profesor_id,
#         grado_id=grado_id
#     ).all()

#     alumnos = Alumno.query\
#         .join(AlumnoGrado)\
#         .filter(AlumnoGrado.grado_id == grado_id)\
#         .all()

#     resumen = {}

#     def obtener_semestre(periodo_id):
#         if periodo_id == 1:
#             return "Primer Trimestre"
#         elif periodo_id == 2:
#             return "Segundo Trimestre"
#         elif periodo_id == 3:
#             return "Tercer Trimestre"
#         else:
#             return f"Periodo {periodo_id}"

#     semestre_actual = obtener_semestre(periodo_id)
#     semestre_siguiente = obtener_semestre(periodo_id + 1)

#     for mp in materias_asignadas:
#         materia_id = mp.materia_id
#         materia_nombre = mp.materia.nombre
#         resumen[materia_nombre] = []

#         for alumno in alumnos:
#             nota_trimestre = NotaTrimestre.query.filter_by(
#                 alumno_id=alumno.id,
#                 materia_id=materia_id,
#                 periodo_id=periodo_id
#             ).first()

#             if not nota_trimestre:
#                 continue

#             nota = nota_trimestre.nota_parcial or 0
#             asistencia = nota_trimestre.asistencia_trimestre or 0
#             participacion = nota_trimestre.participacion_trimestre or 0

#             entrada = np.array([[nota, asistencia, participacion]])
#             predicho = modelo.predict(entrada)[0]
#             clasificacion = clasificar_rendimiento(predicho)

#             prediccion = Prediccion.query.filter_by(
#                 alumno_id=alumno.id,
#                 materia_id=materia_id,
#                 periodo_id=periodo_id + 1
#             ).first()

#             if prediccion:
#                 prediccion.nota_parcial = nota
#                 prediccion.asistencia = asistencia
#                 prediccion.participacion = participacion
#                 prediccion.rendimiento_predicho = float(predicho)
#                 prediccion.clasificacion = clasificacion
#             else:
#                 prediccion = Prediccion(
#                     alumno_id=alumno.id,
#                     materia_id=materia_id,
#                     periodo_id=periodo_id + 1,
#                     nota_parcial=nota,
#                     asistencia=asistencia,
#                     participacion=participacion,
#                     rendimiento_predicho=float(predicho),
#                     clasificacion=clasificacion
#                 )
#                 db.session.add(prediccion)

#             resumen[materia_nombre].append({
#                 "alumno_id": alumno.id,
#                 "alumno": f"{alumno.nombre} {alumno.apellido}",
#                 "nota": nota,
#                 "asistencia": asistencia,
#                 "participacion": participacion,
#                 "prediccion": round(predicho, 2),
#                 "clasificacion": clasificacion
#             })

#     db.session.commit()

#     return jsonify({
#         "mensaje": f"Predicciones generadas para el {semestre_siguiente} del profesor {profesor_id} en grado {grado_id} y periodo {semestre_actual}.",
#         "resumen": resumen
#     })

def generar_predicciones_por_grado_periodo(grado_id, periodo_id):
    materias_asignadas = MateriaGrado.query.filter_by(grado_id=grado_id).all()
    alumnos = Alumno.query.join(AlumnoGrado).filter(AlumnoGrado.grado_id == grado_id).all()

    resumen = {}

    def obtener_trimestre(periodo_id):
        if periodo_id == 1:
            return "1er Trimestre"
        elif periodo_id == 2:
            return "2do Trimestre"
        elif periodo_id == 3:
            return "3er Trimestre"
        else:
            return f"Periodo {periodo_id}"

    trimestre_actual = obtener_trimestre(periodo_id)
    trimestre_siguiente = obtener_trimestre(periodo_id + 1)

    for mg in materias_asignadas:
        materia_id = mg.materia_id
        materia_nombre = mg.materia.nombre
        resumen[materia_nombre] = []

        for alumno in alumnos:
            nota_trimestre = NotaTrimestre.query.filter_by(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id
            ).first()

            if not nota_trimestre:
                continue

            nota = nota_trimestre.nota_parcial or 0
            asistencia = nota_trimestre.asistencia_trimestre or 0
            participacion = nota_trimestre.participacion_trimestre or 0

            entrada = np.array([[nota, asistencia, participacion]])
            predicho = modelo.predict(entrada)[0]
            clasificacion = clasificar_rendimiento(predicho)

            prediccion = Prediccion.query.filter_by(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id + 1
            ).first()

            if prediccion:
                prediccion.nota_parcial = nota
                prediccion.asistencia = asistencia
                prediccion.participacion = participacion
                prediccion.rendimiento_predicho = float(predicho)
                prediccion.clasificacion = clasificacion
            else:
                prediccion = Prediccion(
                    alumno_id=alumno.id,
                    materia_id=materia_id,
                    periodo_id=periodo_id + 1,
                    nota_parcial=nota,
                    asistencia=asistencia,
                    participacion=participacion,
                    rendimiento_predicho=float(predicho),
                    clasificacion=clasificacion
                )
                db.session.add(prediccion)

            resumen[materia_nombre].append({
                "alumno_id": alumno.id,
                "alumno": f"{alumno.nombre} {alumno.apellido}",
                "nota": nota,
                "asistencia": asistencia,
                "participacion": participacion,
                "prediccion": round(predicho, 2),
                "clasificacion": clasificacion
            })

    db.session.commit()

    return jsonify({
        "mensaje": f"Predicciones generadas para el {trimestre_siguiente} del grado {grado_id} basadas en el {trimestre_actual}.",
        "resumen": resumen
    })


def hacer_prediccion_y_guardar(alumno_id, materia_id, periodo_id, nota_parcial, asistencia, participacion):
    entrada = np.array([[nota_parcial, asistencia, participacion]])
    predicho = modelo.predict(entrada)[0]
    clasificacion = clasificar_rendimiento(predicho)

    prediccion = Prediccion.query.filter_by(
        alumno_id=alumno_id,
        materia_id=materia_id,
        periodo_id=periodo_id
    ).first()

    if prediccion:
        # Actualizar si ya existe
        prediccion.nota_parcial = nota_parcial
        prediccion.asistencia = asistencia
        prediccion.participacion = participacion
        prediccion.rendimiento_predicho = float(predicho)
        prediccion.clasificacion = clasificacion
    else:
        # Crear si no existe
        prediccion = Prediccion(
            alumno_id=alumno_id,
            materia_id=materia_id,
            periodo_id=periodo_id,
            nota_parcial=nota_parcial,
            asistencia=asistencia,
            participacion=participacion,
            rendimiento_predicho=float(predicho),
            clasificacion=clasificacion
        )
        db.session.add(prediccion)

    db.session.commit()

    return jsonify({
        "alumno_id": alumno_id,
        "materia_id": materia_id,
        "periodo_id": periodo_id,
        "rendimiento_predicho": round(predicho, 2),
        "clasificacion": clasificacion
    })

def generar_predicciones_para_todos(grado_id, materia_id, periodo_id):
    alumnos = Alumno.query\
        .join(AlumnoGrado)\
        .filter(AlumnoGrado.grado_id == grado_id)\
        .all()

    predicciones_creadas = []

    for alumno in alumnos:
        nota_trimestre = NotaTrimestre.query.filter_by(
            alumno_id=alumno.id,
            materia_id=materia_id,
            periodo_id=periodo_id
        ).first()

        if not nota_trimestre:
            continue

        nota = nota_trimestre.nota_parcial or 0
        asistencia = nota_trimestre.asistencia_trimestre or 0
        participacion = nota_trimestre.participacion_trimestre or 0

        entrada = np.array([[nota, asistencia, participacion]])
        predicho = modelo.predict(entrada)[0]
        clasificacion = clasificar_rendimiento(predicho)

        prediccion = Prediccion.query.filter_by(
            alumno_id=alumno.id,
            materia_id=materia_id,
            periodo_id=periodo_id
        ).first()

        if prediccion:
            prediccion.nota_parcial = nota
            prediccion.asistencia = asistencia
            prediccion.participacion = participacion
            prediccion.rendimiento_predicho = float(predicho)
            prediccion.clasificacion = clasificacion
        else:
            prediccion = Prediccion(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id,
                nota_parcial=nota,
                asistencia=asistencia,
                participacion=participacion,
                rendimiento_predicho=float(predicho),
                clasificacion=clasificacion
            )
            db.session.add(prediccion)

        predicciones_creadas.append(alumno.id)

    db.session.commit()

    return jsonify({
        "mensaje": f"Predicciones generadas para {len(predicciones_creadas)} alumnos.",
        "alumnos": predicciones_creadas
    })

def listar_todas_las_predicciones():
    predicciones = Prediccion.query.all()
    resultado = []
    for p in predicciones:
        resultado.append({
            'id': p.id,
            'alumno_id': p.alumno_id,
            'alumno': p.alumno.nombre,
            'materia_id': p.materia_id,
            'materia': p.materia.nombre,
            'periodo_id': p.periodo_id,
            'periodo': p.periodo.nombre,
            'nota_parcial': p.nota_parcial,
            'asistencia': p.asistencia,
            'participacion': p.participacion,
            'rendimiento_predicho': p.rendimiento_predicho,
            'clasificacion': p.clasificacion
        })
    return jsonify(resultado)


def predicciones_por_alumno(alumno_id):
    # Obtener gestión activa
    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({"error": "No hay gestión activa configurada."}), 400

    # Obtener periodos de esa gestión
    periodos = Periodo.query.filter_by(gestion_id=gestion_activa.id).all()
    periodos_dict = {p.id: p.nombre for p in periodos}

    resultado = {nombre: [] for nombre in periodos_dict.values()}

    for periodo_id, nombre_periodo in periodos_dict.items():
        predicciones = Prediccion.query.filter_by(
            alumno_id=alumno_id,
            periodo_id=periodo_id
        ).all()

        for pred in predicciones:
            nota_real = NotaTrimestre.query.filter_by(
                alumno_id=alumno_id,
                materia_id=pred.materia_id,
                periodo_id=periodo_id
            ).first()

            nota = nota_real.nota_parcial if nota_real else None
            asistencia = nota_real.asistencia_trimestre if nota_real else None
            participacion = nota_real.participacion_trimestre if nota_real else None
            rendimiento_real = calcular_rendimiento_real(nota, asistencia, participacion)

            diferencia = None
            acertado = None
            if rendimiento_real is not None:
                diferencia = round(rendimiento_real - pred.rendimiento_predicho, 2)
                acertado = abs(diferencia) <= 5

            resultado[nombre_periodo].append({
                "materia": pred.materia.nombre,
                "nota_parcial": nota,
                "asistencia": asistencia,
                "participacion": participacion,
                "rendimiento_real": rendimiento_real,
                "rendimiento_predicho": round(pred.rendimiento_predicho, 2),
                "clasificacion": pred.clasificacion,
                "diferencia": diferencia,
                "acertado": acertado
            })

    return jsonify({
        "alumno_id": alumno_id,
        "gestion": gestion_activa.anio,
        "comparacion": resultado
    })





def calcular_rendimiento_real(nota, asistencia, participacion, pesos=PESOS):
    if nota is None:
        return None
    asistencia = asistencia or 0
    participacion = participacion or 0
    return round(nota * pesos[0] + asistencia * pesos[1] + participacion * pesos[2], 2)


































def obtener_predicciones_por_materia():
    periodo_id = request.args.get('periodo_id', type=int)
    materia_id = request.args.get('materia_id', type=int)

    if not periodo_id or not materia_id:
        return jsonify({"error": "Se requieren periodo_id y materia_id"}), 400

    predicciones = Prediccion.query.filter_by(
        periodo_id=periodo_id,
        materia_id=materia_id
    ).all()

    resultado = []
    for pred in predicciones:
        resultado.append({
            "alumno_id": pred.alumno.id,
            "alumno": f"{pred.alumno.nombre} {pred.alumno.apellido}",
            "nota": pred.nota_parcial,
            "asistencia": pred.asistencia,
            "participacion": pred.participacion,
            "prediccion": round(pred.rendimiento_predicho, 2),
            "clasificacion": pred.clasificacion
        })

    return jsonify(resultado)


def listar_materias_del_profesor(profesor_id):
    materias = (
        Materia.query
        .join(MateriaProfesor)
        .filter(MateriaProfesor.profesor_id == profesor_id)
        .distinct()
        .all()
    )

    resultado = [{"id": m.id, "nombre": m.nombre} for m in materias]

    return jsonify(resultado)


