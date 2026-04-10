from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Registrar blueprints
    from App.controllers.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app
