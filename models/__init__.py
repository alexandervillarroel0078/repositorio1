from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# IMPORTA TODOS LOS MODELOS AQUÍ
from .rol import Rol
from .usuario import Usuario

from .gestion import Gestion   
from .grado import Grado
from .periodo import Periodo

from .alumno import Alumno
from .materia import Materia
from .profesor import Profesor
from .ponderaciones_evaluacion import PonderacionEvaluacion
from .alumno_grado import AlumnoGrado
from .materia_grado import MateriaGrado
from .ponderaciones_evaluacion import PonderacionEvaluacion
from .nota_trimestre import NotaTrimestre
from .historial_asistencia_participacion import HistorialAsistenciaParticipacion

from .nivel import Nivel
from .prediccion import Prediccion
from .bitacora import Bitacora
from .inscripicon import Inscripcion