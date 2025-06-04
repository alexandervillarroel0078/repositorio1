from flask import jsonify, request, g
from models import db, Alumno, Gestion
from models.usuario import Usuario
from models.inscripicon import Inscripcion
from werkzeug.security import generate_password_hash, check_password_hash
from traits.bitacora_trait import registrar_bitacora
from utils.token import token_requerido
import jwt
from datetime import datetime

# GET - Listar usuarios
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre_usuario": u.nombre_usuario,
            "correo": u.correo,
            "rol_id": u.rol_id,
            "rol_nombre": u.rol.nombre if u.rol else None,
            "profesor_id": u.profesor_id,
            "profesor_nombre": f"{u.profesor.nombre} {u.profesor.apellido}" if u.profesor else None,
            "alumno_id": u.alumno_id,
            "alumno_nombre": f"{u.alumno.nombre} {u.alumno.apellido}" if u.alumno else None
        } for u in usuarios
    ])


def crear_alumno():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')

        if not nombre or not apellido:
            return jsonify({'error': 'Nombre y apellido son obligatorios'}), 400

        nuevo_alumno = Alumno(nombre=nombre, apellido=apellido)
        db.session.add(nuevo_alumno)
        db.session.commit()

        return jsonify({
            'message': 'Alumno creado exitosamente',
            'alumno': {
                'id': nuevo_alumno.id,
                'nombre': nuevo_alumno.nombre,
                'apellido': nuevo_alumno.apellido
            }
        }), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear alumno', 'details': str(e)}), 500


@token_requerido
def cambiar_password():
    data = request.get_json()
    nueva_contraseña = data.get('nueva_contraseña')

    if not nueva_contraseña:
        return jsonify({'error': 'La nueva contraseña es obligatoria'}), 400

    usuario_id = g.usuario.get('id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    usuario.password_hash = generate_password_hash(nueva_contraseña)
    db.session.commit()

    return jsonify({'mensaje': 'Contraseña actualizada correctamente'}), 200


def inscribir_alumno():
    data = request.get_json()
    alumno_id = data.get('alumno_id')

    if not alumno_id:
        return jsonify({'error': 'El campo alumno_id es obligatorio'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'El alumno no existe'}), 404

    # Buscar gestión activa
    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay una gestión activa'}), 404

    # Verificar si ya está inscrito en esta gestión
    inscripcion_existente = Inscripcion.query.filter_by(
        alumno_id=alumno_id,
        gestion_id=gestion_activa.id
    ).first()

    if inscripcion_existente:
        return jsonify({'error': 'El alumno ya está inscrito en la gestión activa'}), 409

    # Crear inscripción
    nueva_inscripcion = Inscripcion(
        alumno_id=alumno_id,
        gestion_id=gestion_activa.id,
        fecha_inscripcion=datetime.utcnow(),
        estado='activa'
    )

    db.session.add(nueva_inscripcion)
    db.session.commit()

    # 🔐 Crear usuario si no existe
    from werkzeug.security import generate_password_hash
    from models.usuario import Usuario
    from models.rol import Rol

    usuario_existente = Usuario.query.filter_by(alumno_id=alumno_id).first()
    correo_generado = None
    password_asignado = "123456"

    if not usuario_existente:
        correo_generado = f"a{alumno_id}@aula.edu.bo"
        nombre_usuario = correo_generado
        rol_alumno = Rol.query.filter_by(nombre='Alumno').first()
        if not rol_alumno:
            return jsonify({'error': 'Rol de alumno no encontrado'}), 500

        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            password_hash=generate_password_hash(password_asignado),
            correo=correo_generado,
            rol_id=rol_alumno.id,
            alumno_id=alumno_id
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

    return jsonify({
        'mensaje': 'Alumno inscrito correctamente',
        'inscripcion_id': nueva_inscripcion.id,
        'correo_institucional': correo_generado or usuario_existente.correo,
        'contraseña_asignada': password_asignado if correo_generado else 'Ya tenía cuenta'
    }), 201



