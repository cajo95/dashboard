from models.mediciones import *
import datetime
import time

class lectura():
    """ 
    Por excepción de Potencia Activa, todos los demás metodos solo traén el ultimo registro agregado a DB
    Potencia activa además de eso, genera promedio del día actual hasta el ultimo registro, medición más alta
    y sumatoria de consumo.
    """
    def potenciaActiva(self, selector ):
        try:
            acutal = datetime.datetime.now().strftime("%Y-%m-%d")
            listaPotenciaActivaL1 = []
            listaPotenciaActivaL2 = []
            listaPotenciaActivaL3 = []

            if selector == True:
                #potenciaActiva = db.session.query(potencia_activa_m1).order_by(db.session.fecha_hora.desc()).first()
                potenciaActiva = potencia_activa_m1.query.order_by(potencia_activa_m1.fecha_hora.desc()).first()
                potenciaActivaPromedio = potencia_activa_m1.query.order_by(potencia_activa_m1.fecha_hora.desc()) #1

            elif selector == False:
                potenciaActiva = potencia_activa_m2.query.order_by(potencia_activa_m2.fecha_hora.desc()).first()
                potenciaActivaPromedio = db.session.query(potencia_activa_m2).all() #2
                
                #1 y 2 deben ser lista pero no all si no limitadas al día actual.
            
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

        # Obtén la primera instancia de corriente_fase_m1 en la lista de usuarios
        #corrientesFase = corrientesFase[0]

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
    def reporte_de_usuario():

        return
