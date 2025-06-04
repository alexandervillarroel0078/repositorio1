# para local
#  import psycopg2

# def conectar_db():
#     try:
#         conexion = psycopg2.connect(
#             host="localhost",
#             port="5432",
#             database="aulainteligente",
#             user="postgres",
#             password="1234"
#         )
#         return conexion
#     except Exception as e:
#         print("❌ Error al conectar con la base de datos:", e)
#         return None

#produccion /config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:1234@localhost:5432/aulainteligente"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_aula_inteligente")
