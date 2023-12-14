from models.mediciones import *
from sqlalchemy import func, DateTime
from datetime import datetime, timedelta
#from .listas import lista
import pytz
import uuid
import time

class lista():

    def modelos(self):

        lista_modelos = [potencia_activa_m1, potencia_activa_m2, potencia_reactiva_m1, potencia_reactiva_m2,
                        factor_potencia_m1, factor_potencia_m2, corriente_fase_m1, corriente_fase_m2,
                        tension_x_lineas_m1, tension_x_lineas_m2]
        
        return lista_modelos

    def promedios(self, lista_1, lista_2, lista_3):

        promedio_lista_1 = promedio_lista_2 = promedio_lista_3 = 0
        lista_promedios = []

        for valor1, valor2, valor3 in zip(lista_1, lista_2, lista_3):
            promedio_lista_1 += valor1/len(lista_1)
            promedio_lista_2 += valor2/len(lista_2)
            promedio_lista_3 += valor3/len(lista_3)

        #round(totalPotenciaActivaL1, 2)
        promedio_L1 = round(promedio_lista_1, 2)
        promedio_L2 = round(promedio_lista_2, 2)
        promedio_L3 = round(promedio_lista_3, 2)
        
        lista_promedios.append(promedio_L1)
        lista_promedios.append(promedio_L2)
        lista_promedios.append(promedio_L3)

        return lista_promedios

class lectura():
    """ 
    Por excepción de Potencia Activa, todos los demás metodos solo traén el ultimo registro agregado a DB
    Potencia activa además de eso, genera promedio del día actual hasta el ultimo registro, medición más alta
    y sumatoria de consumo.
    """
    def potenciaActiva(self, selector ):
        try:
            acutal = datetime.now().strftime("%Y-%m-%d")
            listaPotenciaActivaL1 = []
            listaPotenciaActivaL2 = []
            listaPotenciaActivaL3 = []

            if selector == True:
                #potenciaActiva = db.session.query(potencia_activa_m1).order_by(db.session.fecha_hora.desc()).first()
                potenciaActiva = potencia_activa_m1.query.order_by(potencia_activa_m1.fecha_hora.desc()).first()
                potenciaActivaPromedio = potencia_activa_m1.query.order_by(potencia_activa_m1.fecha_hora.desc()) #1

            elif selector == False:
                potenciaActiva = potencia_activa_m2.query.order_by(potencia_activa_m2.fecha_hora.desc()).first()
                potenciaActivaPromedio = potencia_activa_m2.query.order_by(potencia_activa_m2.fecha_hora.desc())
                #potenciaActivaPromedio = db.session.query(potencia_activa_m2).all() #2
            
            promedioPotenciaActivaL1 = promedioPotenciaActivaL2 = promedioPotenciaActivaL3 = 0
            totalPotenciaActivaL1 = totalPotenciaActivaL2 = totalPotenciaActivaL3 = 0
            for potencia in potenciaActivaPromedio: 
                potencia_activaL1 = potencia.pot_ac_L1
                potencia_activaL2 = potencia.pot_ac_L2
                potencia_activaL3 = potencia.pot_ac_L3
                fecha_hora        = str(potencia.fecha_hora)
                #print(fecha_hora[0:10])

                if fecha_hora[0:10] == str(acutal):
                    listaPotenciaActivaL1.append(potencia_activaL1)
                    listaPotenciaActivaL2.append(potencia_activaL2)
                    listaPotenciaActivaL3.append(potencia_activaL3)
                    
            for valor1, valor2, valor3 in zip(listaPotenciaActivaL1, listaPotenciaActivaL2, listaPotenciaActivaL3):
                promedioPotenciaActivaL1 += valor1/len(listaPotenciaActivaL1)
                promedioPotenciaActivaL2 += valor2/len(listaPotenciaActivaL2)
                promedioPotenciaActivaL3 += valor3/len(listaPotenciaActivaL3)
                totalPotenciaActivaL1    += valor1
                totalPotenciaActivaL2    += valor2
                totalPotenciaActivaL3    += valor3

            potencia_activaL1 = potenciaActiva.pot_ac_L1
            potencia_activaL2 = potenciaActiva.pot_ac_L2
            potencia_activaL3 = potenciaActiva.pot_ac_L3
            fecha_hora        = potenciaActiva.fecha_hora
            maxL1             = max(listaPotenciaActivaL1)
            maxL2             = max(listaPotenciaActivaL2)
            maxL3             = max(listaPotenciaActivaL3)

            potenciaActiva = {'activa_L1': potencia_activaL1, 
                            'activa_L2'  : potencia_activaL2,
                            'activa_L3'  : potencia_activaL3,
                            'Promedio_L1': round(promedioPotenciaActivaL1, 2),
                            'Promedio_L2': round(promedioPotenciaActivaL2, 2),
                            'Promedio_L3': round(promedioPotenciaActivaL3, 2),
                            'highest_L1' : maxL1,
                            'highest_L2' : maxL2,
                            'highest_L3' : maxL3,
                            'total_L1'   : round(totalPotenciaActivaL1, 2),
                            'total_L2'   : round(totalPotenciaActivaL2, 2),
                            'total_L3'   : round(totalPotenciaActivaL3, 2),
                            'date'       : fecha_hora}
            return potenciaActiva
        except:
            return 0
    
    def potenciaReactiva(self, selector ):
        if selector == True:
            potenciaReactiva = potencia_reactiva_m1.query.order_by(potencia_reactiva_m1.fecha_hora.desc()).first()
        elif selector == False:
            potenciaReactiva = potencia_reactiva_m2.query.order_by(potencia_reactiva_m2.fecha_hora.desc()).first()

        #potenciaReactiva    = potenciaReactiva[0] # Tiene que ser el del día actual de la hora mas reciente.
        potencia_reactivaL1 = potenciaReactiva.pot_rea_L1
        potencia_reactivaL2 = potenciaReactiva.pot_rea_L2
        potencia_reactivaL3 = potenciaReactiva.pot_rea_L3
        fecha_hora          = potenciaReactiva.fecha_hora

        potenciaActiva = {'reactiva_L1' : potencia_reactivaL1, 
                          'reactiva_L2' : potencia_reactivaL2,
                          'reactiva_L3' : potencia_reactivaL3,
                          'fecha_hora'          : fecha_hora}
        
        return potenciaActiva
    
    def factorDePotencia(self, selector):
        if selector == True:
            factorDePotencia = factor_potencia_m1.query.order_by(factor_potencia_m1.fecha_hora.desc()).first()
        elif selector == False:
            factorDePotencia = factor_potencia_m1.query.order_by(factor_potencia_m1.fecha_hora.desc()).first()

        #factorDePotencia    = factorDePotencia[0]
        factorDePotenciaL1 = factorDePotencia.fac_pot_L1
        factorDePotenciaL2 = factorDePotencia.fac_pot_L2
        factorDePotenciaL3 = factorDePotencia.fac_pot_L3
        fecha_hora         = factorDePotencia.fecha_hora

        factorDePotencia = {'FP_L1'     : factorDePotenciaL1, 
                            'FP_L2'     : factorDePotenciaL2,
                            'FP_L3'     : factorDePotenciaL3,
                            'fecha_hora': fecha_hora}
        
        return factorDePotencia
    # Entiendes este fragmento de codigo?    
    def tensionxlineas(self, selector):
        if selector == True:
            voltajeEntreLineas = tension_x_lineas_m1.query.order_by(tension_x_lineas_m1.fecha_hora.desc()).first()
        elif selector == False:
            voltajeEntreLineas = tension_x_lineas_m2.query.order_by(tension_x_lineas_m2.fecha_hora.desc()).first()

        #voltajeEntreLineas = voltajeEntreLineas[0]
        voltajeEntreL1yL2  = voltajeEntreLineas.tension_L1_L2
        voltajeEntreL2yL3  = voltajeEntreLineas.tension_L2_L3
        voltajeEntreL3yL1  = voltajeEntreLineas.tension_L3_L1
        fecha_hora         = voltajeEntreLineas.fecha_hora

        voltajeEntreLineas = {'tension_L1L2' : voltajeEntreL1yL2, 
                              'tension_L2L3' : voltajeEntreL2yL3,
                              'tension_L3L1' : voltajeEntreL3yL1,
                              'fecha_hora'          : fecha_hora}
        
        return voltajeEntreLineas

    def corrientes(self, selector):
        if selector == True:
            corrientesFase = corriente_fase_m1.query.order_by(corriente_fase_m1.fecha_hora.desc()).first()
        elif selector == False:
            corrientesFase = corriente_fase_m2.query.order_by(corriente_fase_m2.fecha_hora.desc()).first()

        # Accede a los valores de los campos de la tabla
        #id_cor = primer_usuario.id_cor
        corriente_L1 = corrientesFase.corriente_L1
        corriente_L2 = corrientesFase.corriente_L2
        corriente_L3 = corrientesFase.corriente_L3
        fecha_hora   = corrientesFase.fecha_hora

        corriente = {'corriente_L1' : corriente_L1, 
                     'corriente_L2' : corriente_L2,
                     'corriente_L3' : corriente_L3,
                     'fecha_hora'   : fecha_hora}

        return corriente
    
class reporte():

    def insert_en_db(self):
        zona_horaria_gmt_5 = pytz.timezone('America/New_York')  
        hora_actual_timeObj = datetime.now(zona_horaria_gmt_5)
        hora_futura_datetimeObj = hora_actual_timeObj + timedelta(hours=1)
        hora_futura_timeObj = hora_futura_datetimeObj.time()
        hora_actual = hora_actual_timeObj.time()
        hora_futura = hora_futura_timeObj
        modelos = lista().modelos()
        promedios = lista()
        lista_promedio_L1 = []
        lista_promedio_L2 = []
        lista_promedio_L3 = []

        # registros_en_rango = potencia_activa_m1.query.filter(
        # potencia_activa_m1.fecha_hora >= datetime.combine(datetime.today(), hora_actual_timeObj.time()),
        # potencia_activa_m1.fecha_hora <= datetime.combine(datetime.today(), hora_futura_timeObj)
        # ).all()

        #if hora_actual_timeObj.minute == 30: 
        for modelo in modelos:
            
            registros_en_rango = modelo.query.filter(
                func.extract('hour', modelo.fecha_hora) >= hora_actual.hour,
                func.extract('hour', modelo.fecha_hora) < hora_futura.hour
            ).order_by(modelo.fecha_hora.asc()).all()

            lista_promedio_L1 = []; lista_promedio_L2 = []; lista_promedio_L3 = []

            if modelo == potencia_activa_m1:
                
                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.pot_ac_L1)
                    lista_promedio_L2.append(iteracion.pot_ac_L2)
                    lista_promedio_L3.append(iteracion.pot_ac_L3)
                
                pro_potactm1 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)
                # print(lista_promedio_L1)
                # print(lista_promedio_L2)
                # print(lista_promedio_L3)
                 
            elif modelo == potencia_activa_m2:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.pot_ac_L1)
                    lista_promedio_L2.append(iteracion.pot_ac_L2)
                    lista_promedio_L3.append(iteracion.pot_ac_L3)

                pro_potactm2 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)           

            elif modelo == potencia_reactiva_m1:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.pot_rea_L1)
                    lista_promedio_L2.append(iteracion.pot_rea_L2)
                    lista_promedio_L3.append(iteracion.pot_rea_L3)

                pro_potreactm1 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == potencia_reactiva_m2:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.pot_rea_L1)
                    lista_promedio_L2.append(iteracion.pot_rea_L2)
                    lista_promedio_L3.append(iteracion.pot_rea_L3)

                pro_potreactm2 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)
                
            elif modelo == factor_potencia_m1:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.fac_pot_L1)
                    lista_promedio_L2.append(iteracion.fac_pot_L2)
                    lista_promedio_L3.append(iteracion.fac_pot_L3)

                pro_factpotm1 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == factor_potencia_m2:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.fac_pot_L1)
                    lista_promedio_L2.append(iteracion.fac_pot_L2)
                    lista_promedio_L3.append(iteracion.fac_pot_L3)

                pro_factpotm2 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == corriente_fase_m1:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.corriente_L1)
                    lista_promedio_L2.append(iteracion.corriente_L2)
                    lista_promedio_L3.append(iteracion.corriente_L3)

                pro_corrientem1 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == corriente_fase_m2:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.corriente_L1)
                    lista_promedio_L2.append(iteracion.corriente_L2)
                    lista_promedio_L3.append(iteracion.corriente_L3)

                pro_corrientem2 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == tension_x_lineas_m1:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.tension_L1_L2)
                    lista_promedio_L2.append(iteracion.tension_L2_L3)
                    lista_promedio_L3.append(iteracion.tension_L3_L1)

                pro_tensionm1 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)

            elif modelo == tension_x_lineas_m2:

                for iteracion in registros_en_rango:
                    lista_promedio_L1.append(iteracion.tension_L1_L2)
                    lista_promedio_L2.append(iteracion.tension_L2_L3)
                    lista_promedio_L3.append(iteracion.tension_L3_L1)

                pro_tensionm2 = promedios.promedios(lista_promedio_L1, lista_promedio_L2, lista_promedio_L3)
        
        fechahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_pot_act = promedios_por_horas(id_promedio = str(uuid.uuid4()), fecha_hora = fechahora,
                                            pot_act_L1_m1 = pro_potactm1[0], pot_act_L2_m1 = pro_potactm1[1], pot_act_L3_m1 = pro_potactm1[2],
                                            pot_act_L1_m2 = pro_potactm2[0], pot_act_L2_m2 = pro_potactm2[1], pot_act_L3_m2 = pro_potactm2[2],
                                            pot_react_L1_m1 = pro_potreactm1[0], pot_react_L2_m1 = pro_potreactm1[1], pot_react_L3_m1 = pro_potreactm1[2],
                                            pot_react_L1_m2 = pro_potreactm2[0], pot_react_L2_m2 = pro_potreactm2[1], pot_react_L3_m2 = pro_potreactm2[2],
                                            fac_pot_L1_m1 = pro_factpotm1[0], fac_pot_L2_m1 = pro_factpotm1[1], fac_pot_L3_m1 = pro_factpotm1[2],
                                            fac_pot_L1_m2 = pro_factpotm2[0], fac_pot_L2_m2 = pro_factpotm2[1], fac_pot_L3_m2 = pro_factpotm2[2],
                                            corriente_L1_m1 = pro_corrientem1[0], corriente_L2_m1 = pro_corrientem1[1], corriente_L3_m1 = pro_corrientem1[2],
                                            corriente_L1_m2 = pro_corrientem2[0], corriente_L2_m2 = pro_corrientem2[1], corriente_L3_m2 = pro_corrientem2[2],
                                            tension_L1L2_m1 = pro_tensionm1[0], tension_L2L3_m1 = pro_tensionm1[1], tension_L3L1_m1 = pro_tensionm1[2],
                                            tension_L1L2_m2 = pro_tensionm2[0], tension_L2L3_m2 = pro_tensionm2[1], tension_L3L1_m2 = pro_tensionm2[2],
                                            )
        #print('chichichi')
        db.session.add(insert_pot_act)
        db.session.commit()

    
    def grafica_reporte_basico(self, selector, fecha_recibida): 
        lista_potencia_activa_por_hora = []
        fecha_recibida = datetime.strptime(fecha_recibida, '%Y-%m-%d')
        fecha_hora_actual = datetime.now()
        fecha_hora_anterior = fecha_hora_actual - timedelta(hours=1) # Calcula la fecha y hora anterior
        promedios_por_horas.fecha_hora = func.cast(promedios_por_horas.fecha_hora, DateTime) # Convierte la columna 'fecha_hora' a tipo datetime

        if selector == True:
            # Trae el registro generado cada hora, el registro se guardará cada minuto 59:59 de cada hora
            # en la tabla 'promedios_por_horas' esta función se ejecutará a las 00:00 de cada hora.
            # La función también se ejecutará cada vez que se envíe una fecha de la que se llamará 
            # TODOS los registros, eso lo hace la consultá en el else. 
            Select_potencia_Activa_m1 = promedios_por_horas.query.filter(
                promedios_por_horas.fecha_hora.between(fecha_hora_anterior, fecha_hora_actual)
            ).order_by(promedios_por_horas.fecha_hora.desc()).all()
        else:
            # Trae todos los registros de promedios del dia 'fecha_recibida'
            Select_potencia_Activa_m1 = promedios_por_horas.query.filter(
                db.func.date(promedios_por_horas.fecha_hora) == fecha_recibida.date()
            ).order_by(promedios_por_horas.fecha_hora.desc()).all()

        for iterador in Select_potencia_Activa_m1:
            lista_potencia_activa_por_hora.append(iterador.pot_act_L1_m1)
            lista_potencia_activa_por_hora.append(iterador.pot_act_L2_m1)
            lista_potencia_activa_por_hora.append(iterador.pot_act_L3_m1)
            lista_potencia_activa_por_hora.append(iterador.pot_act_L1_m2)
            lista_potencia_activa_por_hora.append(iterador.pot_act_L2_m2)
            lista_potencia_activa_por_hora.append(iterador.pot_act_L3_m2)
            lista_potencia_activa_por_hora.append(iterador.fecha_hora)

        return lista_potencia_activa_por_hora
    
    # Una vez con la información, se saca el consumo más alto, el más bajo y sumatoria por linea.
    # ademas tambien consumo promedio de las tres lineas: sumar el consumo total de las 3 lineas y promediar
    # y por ultimo consumo total de las tres lineas: suma de consumo total de las 3 lineas.

    def operaciones(self, lista):
        lista_operaciones = []
        maximo = max(lista)
        minimo = min(lista)
        suma   = sum(lista)
        lista_operaciones.append(maximo)
        lista_operaciones.append(minimo)
        lista_operaciones.append(suma)
        return lista_operaciones
    
    def operaciones_reporte_basico(self, selector, fecha_recibida):
        
        operaciones_enlistadas = 0
        reportes = reporte()
        fecha_actual = datetime.now().date()
        fecha_inicio_dia_actual = datetime.combine(fecha_actual, datetime.min.time())
        fecha_fin_dia_actual = datetime.combine(fecha_actual, datetime.max.time())
        fecha_recibida = datetime.strptime(fecha_recibida, '%Y-%m-%d')
        lista_pot_act_L1m1 = []; lista_pot_act_L2m1 = []; lista_pot_act_L3m1 = []
        lista_pot_act_L1m2 = []; lista_pot_act_L2m2 = []; lista_pot_act_L3m2 = []
        
        if selector == True:
             # La consulta filtra los registros y trae solo los de la fecha recibida desde el endpoint.
            lista_reporte = promedios_por_horas.query.filter(
                promedios_por_horas.fecha_hora.between(fecha_inicio_dia_actual, fecha_fin_dia_actual)
            ).order_by(promedios_por_horas.fecha_hora.desc()).all()
        else:
            # La consulta filtra los registros y trae solo los de la fecha actual.
            lista_reporte = promedios_por_horas.query.filter(
                db.func.date(promedios_por_horas.fecha_hora) == fecha_recibida.date()
            ).order_by(promedios_por_horas.fecha_hora.desc()).all()

        for iterador in lista_reporte:
            lista_pot_act_L1m1.append(iterador.pot_act_L1_m1)
            lista_pot_act_L2m1.append(iterador.pot_act_L2_m1)
            lista_pot_act_L3m1.append(iterador.pot_act_L3_m1)
            lista_pot_act_L1m2.append(iterador.pot_act_L1_m2)
            lista_pot_act_L2m2.append(iterador.pot_act_L2_m2)
            lista_pot_act_L3m2.append(iterador.pot_act_L3_m2)

        pot_act_L1m1 = reportes.operaciones(lista_pot_act_L1m1)
        pot_act_L2m1 = reportes.operaciones(lista_pot_act_L2m1)
        pot_act_L3m1 = reportes.operaciones(lista_pot_act_L3m1)
        pot_act_L1m2 = reportes.operaciones(lista_pot_act_L1m2)
        pot_act_L2m2 = reportes.operaciones(lista_pot_act_L2m2)
        pot_act_L3m2 = reportes.operaciones(lista_pot_act_L3m2)        
        consumo_total_lineas_m1 = pot_act_L1m1[2] + pot_act_L2m1[2] + pot_act_L3m1[2]
        consumo_prome_lineas_m1 = consumo_total_lineas_m1 / 3
        consumo_total_lineas_m2 = pot_act_L1m2[2] + pot_act_L2m2[2] + pot_act_L3m2[2]
        consumo_prome_lineas_m2 = consumo_total_lineas_m2 / 3
        #TODO hacer redondeo de totales y promedios; hacer repaso de toda la logica.

        operaciones_enlistadas = {'operacionesL1m1': pot_act_L1m1, 
                                'operacionesL2m1' : pot_act_L2m1,
                                'operacionesL3m1' : pot_act_L3m1,
                                'operacionesL1m2' : pot_act_L1m2,
                                'operacionesL2m2' : pot_act_L2m2,
                                'operacionesL3m2' : pot_act_L3m2,
                                'consumo_total_lineas_m1' : consumo_total_lineas_m1,
                                'consumo_total_lineas_m2' : consumo_total_lineas_m2,
                                'consumo_prome_lineas_m1' : consumo_prome_lineas_m1,
                                'consumo_prome_lineas_m2' : consumo_prome_lineas_m2,}
        
        return operaciones_enlistadas
        
    def reporte_otro_dia(self, fecha_recibida):
        reportes = reporte()
        reporte_grafica = reportes.grafica_reporte_basico(False, fecha_recibida)
        reporte_operaciones = reportes.operaciones_reporte_basico(False, fecha_recibida)

        operaciones_enlistadas = {'reporte_grafica': reporte_grafica, 
                                'reporte_operaciones' : reporte_operaciones}

        return operaciones_enlistadas

    def reporte_avanzado(self):

        return
    