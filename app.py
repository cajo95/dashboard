from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la primera base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:950221@localhost/medidor"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# el método SQLAlchemy(app) llama implícitamente al método init_app()
db = SQLAlchemy(app) #instancia de SQLAlchemy vinculada a tu aplicación Flask.

from routes.mediciones import dashboard_blueprint, reporte_blueprint
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(reporte_blueprint)