from flask import Flask
from models.employee import db
from routes.attendance_routes import attendance_blueprint
from flask_cors import CORS
from flask_migrate import Migrate

# Crear instancia Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Registrar rutas
app.register_blueprint(attendance_blueprint)

# Ejecutar aplicación
if __name__ == '__main__':
    app.run(debug=True)
