import os
from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_migrate import Migrate

from models.employee import db
from routes.attendance_routes import attendance_blueprint
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.usuario import usuario_bp
from blueprints.report import report_bp  # Blueprint de reportes

app = Flask(__name__)

app.secret_key = 'pinchellave'

# 🔧 Configuración MySQL (recomendado usar base de datos remota en Render)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'login')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Asignar instancia de MySQL a blueprints
import blueprints.auth
import blueprints.admin

blueprints.auth.mysql = mysql
blueprints.admin.mysql = mysql

# 🔧 Configuración SQLAlchemy para asistencia (usar SQLite temporalmente)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# 📌 Registro de Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(attendance_blueprint)
app.register_blueprint(report_bp)

# Rutas
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('auth.welcome'))

@app.route('/admin')
def admin_dashboard():
    return redirect(url_for('admin.dashboard'))

# 🟢 Agregado: correr con puerto dinámico para Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
