from flask import Blueprint, request, jsonify
#from app import db
#from models.usuario import Usuario
#from models.mediciones import corriente_fase_m1
from clases.clases import lectura, reporte
from datetime import datetime

dashboard_blueprint = Blueprint('dashboard', __name__)
reporte_blueprint = Blueprint('reporte', __name__)
fecha_actual = datetime.now().date()
lecturas = lectura()
reportes = reporte()

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
@reporte_blueprint.route('/report', methods=['POST'])
def reporte_sencillo_dia_actual():
    fecha_generica = "1999-12-31"
    # Estas listas contienen los elementos para la grafica y el reporte sencillo de cada hora.
    lista2grafica = reportes.grafica_reporte_basico(True, fecha_generica)
    lista2operaciones = reportes.operaciones_reporte_basico(True, fecha_generica)
    reporte_avanzado = reportes.reporte_avanzado(True, fecha_generica)

    return jsonify({'lista_grafica': lista2grafica},
                    {'lista_operaciones': lista2operaciones},
                    {'repore_avanzado': reporte_avanzado})

@reporte_blueprint.route('/reportother', methods=['POST'])
def reporte_cualquier_dia():
    # Este endpoint permite traer todos los registros de la tabla 'promedios_por_hora'

    global fecha_actual
    data = request.get_json()
    fecha_recibida = data['fecha']
    lista2grafica = reportes.reporte_otro_dia(fecha_recibida)
    return jsonify(lista2grafica)

    #if str(fecha_recibida) == str(fecha_actual):
        #print(fecha_recibida)

    
    # else:
    #     return jsonify({'reportother': False})
    
"""Reporte avanzado debe ir dentro de reporte sencillo en el mismo JSON
    Tanto el de fecha de dia actual como cualquier dia"""
    
# @reporte_blueprint.route('/advance', methods=['POST'])
# def reporte_avanzado():
#     global fecha_actual
#     data = request.get_json()
#     fecha_recibida = data['fecha']
#     lista2grafica = reportes.reporte_otro_dia(fecha_recibida)
#     return jsonify(lista2grafica)

    #return jsonify({'report': 'advance'})