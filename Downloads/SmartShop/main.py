from App import create_app
from flask import render_template

app = create_app()

@app.route('/')
def home():
    """Página de inicio - Redirige a login o dashboard"""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard de la aplicación"""
    return render_template('dashboard.html')

@app.route('/login')
def login_page():
    """Página de login"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Página de registro"""
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
