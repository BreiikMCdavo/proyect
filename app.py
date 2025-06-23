from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_migrate import Migrate

from models.employee import db
from routes.attendance_routes import attendance_blueprint
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.usuario import usuario_bp
from blueprints.report import report_bp  # Importa tu blueprint de reportes

app = Flask(__name__)

app.secret_key = 'pinchellave'

# Configuración MySQL para login y usuarios
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Crear instancia MySQL aquí
mysql = MySQL(app)

# Asignar mysql a blueprints que lo necesitan
import blueprints.auth
import blueprints.admin

blueprints.auth.mysql = mysql
blueprints.admin.mysql = mysql

# Configuración SQLAlchemy para asistencia
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db y migraciones antes de registrar blueprints
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Registrar blueprints SOLO UNA VEZ cada uno
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(attendance_blueprint)
app.register_blueprint(report_bp)  # <-- Aquí el blueprint de reportes

@app.route('/')
def home():
    print("Entró a la ruta raíz '/'")
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    print("Entró a la ruta '/dashboard'")
    return redirect(url_for('auth.welcome'))
@app.route('/admin')
def admin_dashboard():                  
    print("Entró a la ruta '/admin'")
    return redirect(url_for('admin.dashboard'))     