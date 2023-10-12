from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la primera base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:950221@localhost/medidor1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la segunda base de datos utilizando SQLALCHEMY_BINDS
app.config['SQLALCHEMY_BINDS'] = {
    'medidor2': "mysql://root:950221@localhost/medidor2"}

db = SQLAlchemy(app) #instancia de SQLAlchemy vinculada a tu aplicación Flask.

from routes.mediciones import mediciones_blueprint
app.register_blueprint(mediciones_blueprint)





