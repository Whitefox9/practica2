from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from App import db
from App.models.user import User
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# Regex para validar email
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo usuario
    Requiere: nuevo_usuario, nuevo_email, nuevo_password
    """
    try:
        data = request.get_json()
        
        # Validaciones
        usuario = data.get('nuevo_usuario', '').strip()
        email = data.get('nuevo_email', '').strip()
        password = data.get('nuevo_password', '')
        
        if not all([usuario, email, password]):
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'}), 400
        
        if len(usuario) < 3:
            return jsonify({'success': False, 'message': 'El usuario debe tener al menos 3 caracteres'}), 400
        
        if not re.match(EMAIL_REGEX, email):
            return jsonify({'success': False, 'message': 'Email inválido'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres'}), 400
        
        # Verificar si el usuario o email ya existe
        if User.query.filter_by(usuario=usuario).first():
            return jsonify({'success': False, 'message': 'El usuario ya existe'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409
        
        # Crear nuevo usuario
        nuevo_usuario = User(usuario=usuario, email=email)
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Usuario registrado exitosamente',
            'user': nuevo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error en el servidor: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión de un usuario
    Requiere: usuario, password
    """
    try:
        data = request.get_json()
        
        usuario = data.get('usuario', '').strip()
        password = data.get('password', '')
        
        if not usuario or not password:
            return jsonify({'success': False, 'message': 'Usuario y contraseña son requeridos'}), 400
        
        # Buscar usuario por nombre de usuario
        user = User.query.filter_by(usuario=usuario).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401
        
        # Crear sesión
        session['user_id'] = user.id
        session['usuario'] = user.usuario
        session.permanent = True
        
        return jsonify({
            'success': True, 
            'message': 'Sesión iniciada correctamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error en el servidor: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Cierra la sesión del usuario
    """
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Sesión cerrada'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error en el servidor: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Obtiene el perfil del usuario autenticado
    """
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'No autenticado'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            session.clear()
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error en el servidor: {str(e)}'}), 500


@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """
    Verifica si el usuario está autenticado
    """
    user_id = session.get('user_id')
    
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({
        'success': True,
        'authenticated': False
    }), 200
