from flask import Blueprint, jsonify
#from app import db
#from models.usuario import Usuario
#from models.mediciones import corriente_fase_m1
from clases.clases import lectura

mediciones_blueprint = Blueprint('mediciones', __name__)
lecturas = lectura()

@mediciones_blueprint.route('/dashboardm1', methods=['POST'])
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

@mediciones_blueprint.route('/dashboardm2', methods=['POST'])
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

@mediciones_blueprint.route('/reporte', methods=['POST'])
def reporte():

    return

@mediciones_blueprint.route('/info', methods=['POST'])
def info():

    return