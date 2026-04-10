import os
from datetime import timedelta

# Obtener la ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuración basica
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-desarrollo'
    
    # Configuración de SQLite - BD en la raíz del proyecto
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "smartshop.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
