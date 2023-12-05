from flask import Blueprint, request, jsonify
#from app import db
#from models.usuario import Usuario
#from models.mediciones import corriente_fase_m1
from clases.clases import lectura, reporte
from datetime import datetime

dashboard_blueprint = Blueprint('dashboard', __name__)
reporte_blueprint = Blueprint('reporte', __name__)
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

# ESTA CONSULTA DEBE SER HECHA CADA INICIO DE HORA 06:00, 07:00... ETC.
# A DIFERENCIA DE LA INSERSIÓN DE LOS PROMEDIOS QUE SE PROGRAMA PARA CADA FINAL DE HORA: 06:59:59 COMO TAREA PROGRAMADA
@reporte_blueprint.route('/reporte', methods=['POST'])
def reporte_sencillo():
    lista2grafica = reporte().grafica_reporte_basico()
    lista2operaciones = reporte().operaciones_reporte_basico()
    try:
        fecha_seleccionada = request.args.get('fecha')

        if str(fecha_seleccionada) == str(datetime.now().date()): # validar que se puedan comparar eficientemente.
            return jsonify({'lista_grafica': lista2grafica},
                           {'lista_operaciones': lista2operaciones})

        else:
            # Aqui va la logica de cuando la consulta es en cualquier día actual anterior al actual.
            pass

        return

    except:
        return

# @reporte_blueprint.route('/reportebasico', methods=['POST'])
# def reporte_sencillo():

    

#     return jsonify({'Potencia': lista2grafica})
