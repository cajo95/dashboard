from models.mediciones import *
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

