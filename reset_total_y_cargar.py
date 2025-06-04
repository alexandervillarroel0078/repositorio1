import csv
from flask import Flask
from models import db

# SISTEMA GENERAL
from models.rol import Rol
from models.usuario import Usuario

# SISTEMA DE ALUMNOS

# SISTEMA ACADÉMICO
from models.gestion import Gestion
from models.grado import Grado
from models.periodo import Periodo

from models.nivel   import Nivel
from models.materia import Materia  
from models.profesor import Profesor
from models.alumno import Alumno

from models.periodo import Periodo
from models.ponderaciones_evaluacion import PonderacionEvaluacion
from models.materia_grado import MateriaGrado 
from models.alumno_grado import AlumnoGrado
from models.materia_profesor import MateriaProfesor

from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion

from models.nota_trimestre import NotaTrimestre
from models.prediccion import Prediccion

from models.bitacora import Bitacora
from sqlalchemy import text




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/aulainteligente'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def cargar_csv(Modelo, archivo):
    db.session.query(Modelo).delete()
    db.session.commit()

    with open(archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if v in ("", "null", None):
                    clean_row[k] = None
                elif v.lower() == "true":
                    clean_row[k] = True
                elif v.lower() == "false":
                    clean_row[k] = False
                elif v.isdigit():
                    clean_row[k] = int(v)
                else:
                    try:
                        clean_row[k] = float(v) if '.' in v else v
                    except:
                        clean_row[k] = v
            instancia = Modelo(**clean_row)
            db.session.add(instancia)
        db.session.commit()
        print(f"✅ Datos cargados en: {Modelo.__tablename__}")


with app.app_context():
    #  1. Eliminar todas las tablas
    db.drop_all()
    print("🧹 Todas las tablas eliminadas")

    #  2. Crear tablas nuevamente
    db.create_all()
    print("✅ Tablas creadas")

    #  3. Insertar datos desde CSVs
    cargar_csv(Gestion, 'scripts/gestion_utf8.csv')
    cargar_csv(Rol, 'scripts/rol_utf8.csv')
    cargar_csv(Nivel, 'scripts/nivel_utfo.csv')
    cargar_csv(Grado, 'scripts/grado_utf8.csv')
    cargar_csv(Materia, 'scripts/materia_utf8.csv')
    
    cargar_csv(Periodo, 'scripts/periodo_utf8.csv')
    cargar_csv(Profesor, 'scripts/profesor_utf8.csv')
    cargar_csv(Alumno, 'scripts/alumno_utf8.csv')
    
    cargar_csv(AlumnoGrado, 'scripts/alumno_grado_utf8.csv')
    cargar_csv(PonderacionEvaluacion, 'scripts/ponderaciones_evaluacion_uft8.csv')
    
    cargar_csv(HistorialAsistenciaParticipacion, 'scripts/historial_asistencia_participacion_utf8.csv')
    cargar_csv(NotaTrimestre, 'scripts/nota_trimestre_utf8.csv')
    cargar_csv(MateriaProfesor, 'scripts/materia_profesor_utf8.csv')
    cargar_csv(MateriaGrado, 'scripts/materia_grado_utf8.csv')

    cargar_csv(Prediccion, 'scripts/prediccion_utf8.csv')
    cargar_csv(Bitacora, 'scripts/bitacora_utf8.csv')
    cargar_csv(Usuario, 'scripts/usuario_utf8.csv')
    
    # 4. Ajustar las secuencias después de cargar CSVs
    from sqlalchemy import text
    db.session.execute(text("SELECT setval('alumnos_id_seq', COALESCE((SELECT MAX(id) FROM alumnos), 1))"))
    db.session.commit()
    print("🔄 Secuencia 'alumnos_id_seq' ajustada correctamente")

# DO $$ DECLARE
#     r RECORD;
# BEGIN
#     -- Desactivar temporalmente restricciones
#     EXECUTE 'SET session_replication_role = replica';

#     -- Eliminar todas las tablas del esquema público
#     FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
#         EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
#     END LOOP;

#     -- Restaurar las restricciones
#     EXECUTE 'SET session_replication_role = origin';
# END $$;
