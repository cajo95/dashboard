from flask import Blueprint, jsonify
#from app import db
#from models.usuario import Usuario
#from models.mediciones import corriente_fase_m1
from clases.clases import lectura
from datetime import datetime

dashboard_blueprint = Blueprint('dashboard', __name__)
reporte_blueprint = Blueprint('dashboard', __name__)
lecturas = lectura()

@dashboard_blueprint.route('/dashboardm1', methods=['POST'])
def dashboard_m1():
    selector = True
    corrientes       = lecturas.corrientes(selector)
    potenciaActiva   = lecturas.potenciaActiva(selector)
    potemciaReactiva = lecturas.potenciaReactiva(selector)
    factorDePotencia = lecturas.factorDePotencia(selector)
    tensionxLineas   = lecturas.tensionxlineas(selector)
    diccionario = jsonify({'Potencia Activa':potenciaActiva,
                            'Potencia Reactiva': potemciaReactiva,
                            'Factor de potencia': factorDePotencia,
                            'Tensión por lineas': tensionxLineas,
                            'Corriente por linea': corrientes,})
                            # consumo promedio del día por potencia activa

    return diccionario

@dashboard_blueprint.route('/dashboardm2', methods=['POST'])
def dashboard_m2():
    selector = False
    corrientes       = lecturas.corrientes(selector)
    potenciaActiva   = lecturas.potenciaActiva(selector)
    potemciaReactiva = lecturas.potenciaReactiva(selector)
    factorDePotencia = lecturas.factorDePotencia(selector)
    tensionxLineas   = lecturas.tensionxlineas(selector)
    diccionario = jsonify({'Potencia Activa':potenciaActiva,
                            'Potencia Reactiva': potemciaReactiva,
                            'Factor de potencia': factorDePotencia,
                            'Tensión por lineas': tensionxLineas,
                            'Corriente por linea': corrientes,})
    
    return diccionario

@reporte_blueprint.route('/reporte', methods=['POST'])
def reporte():
    hora = datetime.now().time()
    
    return

@reporte_blueprint.route('/info', methods=['POST'])
def info():

    return

hora = datetime.now().time()