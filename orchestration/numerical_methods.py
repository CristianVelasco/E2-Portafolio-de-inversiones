# Standard library imports
import os
import warnings

# Third party imports
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

# class FronteraEficiente():

#     def __init__(self):
#         pass

#     def load_df_portafolio(self, path_processed: str, date_last: str) -> pd.DataFrame:

#         portafolio = pd.read_csv(f"{path_processed}/Portafolio_{date_last}.csv")

#         portafolio = portafolio.filter(like='Rendimiento')

#         portafolio = portafolio.iloc[1:].reset_index(drop=True)
        
#         return portafolio
    
    
#     def transformationyfinance_2(self, df: pd.DataFrame) -> pd.DataFrame:

#         """
#         Este metodo retorna el rendimiento del portafolio con pesos iniciales distribuidos igualmente

#         Args:
#             df (pd.Dataframe) : Dataframe con los valores de cierre y rendimientos logaritmicos calculados

#         Return: 
#             pd.DataFrame : Retorna un dataframe con los rendimientos y volatilidades 
#             diarias y anualizadas para las acciones y el portafolio 
#         """
#         df_rend = df
        
#         #Numero de activos
#         n_assets = df_rend.shape[1]

#         # pesos iguales
#         w = np.array([1 / n_assets] * n_assets)  

#         df_portafolio = df_rend.values.dot(w)
#         df_rend['Portafolio'] = df_portafolio

#         # Calcular estadísticas
#         promedio_diario = df_rend.mean()
#         promedio_anual = promedio_diario * 252

#         desv_std_diaria = df_rend.std()
#         desv_std_anual = desv_std_diaria * np.sqrt(252)

        
#         df_portafolio_resume = pd.DataFrame({
#             'Rentabilidad Diaria': promedio_diario,
#             'Rentabilidad Anual': promedio_anual,
#             'Volatilidad Diaria': desv_std_diaria,
#             'Volatilidad Anual': desv_std_anual
#         }) 

#         print("\nResumen del Portafolio (incluye activos y portafolio):\n")
#         print(df_portafolio_resume.T.round(6))

#         return df_portafolio_resume

#     def list_volatilidad(self, df: pd.DataFrame) -> list:

#         linspace_resultado = np.linspace(df['Volatilidad Anual'].min(), df['Volatilidad Anual'].max(), 20)

#         print(linspace_resultado)

#         return linspace_resultado
    
    
#     def maxifrontera(self, df: pd.DataFrame, linspace_resultado: list) -> list:


#         """Este metodo retorna una lista de pesos, donde maximimiza la rentabilidad anualiazda de las acciones
#             (promedio anualizado), lista de n pesos, la sumatoria de estos pesos es 1
#             Args:

#             Returns:
#                 list
#         """

#         rendimiento = []

#         lista_volatilidad = linspace_resultado

#         for voaltilidad in lista_volatilidad:

#             # Numero de acciones
#             n_assets = df.shape[1]

#             # Función objetivo: maximizar retorno anualizado
#             def funcion_objetivo(pesos):
#                 retorno = np.mean(np.dot(df, pesos))
                
#                 return - (retorno * 252)

#             # Restricción 1: suma de los pesos == 1
#             restriccion_suma = {'type': 'eq', 'fun': lambda pesos: np.sum(pesos) - 1}

#             # Restricción 2: volatilidad anualizada == umbral
#             umbral_volatilidad = voaltilidad
#             restriccion_vol = {
#                 'type': 'eq',
#                 'fun': lambda pesos: (np.std(np.dot(df, pesos)) * np.sqrt(252)) - umbral_volatilidad
#             }

#             # Límites para los pesos
#             boundaries = [(0, 1) for _ in range(n_assets)]

#             # Pesos iniciales iguales
#             pesos_iniciales = np.array([1 / n_assets] * n_assets)

#             # Optimización
#             resultado = minimize(
#                 funcion_objetivo,
#                 pesos_iniciales,
#                 method='SLSQP',
#                 bounds=boundaries,
#                 constraints=[restriccion_suma, restriccion_vol]
#             )
#             rendimiento.append(-resultado.fun)

#         return rendimiento 
    
#     def grafico_frontera_eficiente(self, df: pd.DataFrame, linspace_resultado: list):

#         lista_rendimineto = self.maxifrontera(df, linspace_resultado)
#         lista_volatilidad = linspace_resultado

#         df_frontera = pd.DataFrame({
#             'Rentabilidad Anual': lista_rendimineto,
#             'Volatilidad Anual': lista_volatilidad,
#         })

#         sns.set(style="whitegrid", context="notebook")

#         plt.figure(figsize=(12, 7))

#         # 🔵 Puntos azules pequeños
#         sns.scatterplot(
#             x='Volatilidad Anual',
#             y='Rentabilidad Anual',
#             data=df_frontera,
#             color='royalblue',
#             s=30,  # tamaño reducido
#             label='Portafolios',
#             edgecolor='black'
#         )

#         # ⚫ Línea negra, delgada y discontinua
#         sns.lineplot(
#             x='Volatilidad Anual',
#             y='Rentabilidad Anual',
#             data=df_frontera,
#             color='black',
#             linewidth=1,
#             linestyle='--',
#             label='Frontera Eficiente'
#         )

#         plt.title('Frontera Eficiente del Portafolio', fontsize=16, fontweight='bold')
#         plt.xlabel('Volatilidad Anual', fontsize=12)
#         plt.ylabel('Rentabilidad Anual', fontsize=12)
#         plt.legend(fontsize=10)
#         plt.grid(True, linestyle='--', alpha=0.5)
#         plt.tight_layout()
#         plt.show()


class Sharperatio():

    def __init__(self):
        pass


    def load_df_portafolio(self, path_processed: str, date_last: str) -> pd.DataFrame:

        portafolio = pd.read_csv(f"{path_processed}/Portafolio_{date_last}.csv")

        portafolio = portafolio.filter(like='Rendimiento')

        portafolio = portafolio.iloc[1:].reset_index(drop=True)

        print(portafolio)
        
        return portafolio
    
    def transformationyfinance_2(self, df: pd.DataFrame) -> pd.DataFrame:

        """
        Este metodo retorna el rendimiento del portafolio con pesos iniciales distribuidos igualmente

        Args:
            df (pd.Dataframe) : Dataframe con los valores de cierre y rendimientos logaritmicos calculados

        Return: 
            pd.DataFrame : Retorna un dataframe con los rendimientos y volatilidades 
            diarias y anualizadas para las acciones y el portafolio 
        """
        df_rend = df
        
        #Numero de activos
        n_assets = df_rend.shape[1]

        # pesos iguales
        w = np.array([1 / n_assets] * n_assets)  

        df_portafolio = df_rend.values.dot(w)
        df_rend['Portafolio'] = df_portafolio

        # Calcular estadísticas
        promedio_diario = df_rend.mean()
        promedio_anual = promedio_diario * 252

        desv_std_diaria = df_rend.std()
        desv_std_anual = desv_std_diaria * np.sqrt(252)

        
        df_portafolio_resume = pd.DataFrame({
            'Rentabilidad Diaria': promedio_diario,
            'Rentabilidad Anual': promedio_anual,
            'Volatilidad Diaria': desv_std_diaria,
            'Volatilidad Anual': desv_std_anual
        }) 

        print("\nResumen del Portafolio (incluye activos y portafolio):\n")
        print(df_portafolio_resume.T.round(6))

        return df_portafolio_resume

    def list_volatilidad(self, df: pd.DataFrame) -> list:

        linspace_resultado = np.linspace(df['Volatilidad Anual'].min(), df['Volatilidad Anual'].max(), 20)

        # print(linspace_resultado)

        return linspace_resultado
    
    def maxifrontera(self, df: pd.DataFrame, linspace_resultado: list) -> list:


        """Este metodo retorna una lista de pesos, donde maximimiza la rentabilidad anualiazda de las acciones
            (promedio anualizado), lista de n pesos, la sumatoria de estos pesos es 1
            Args:

            Returns:
                list
        """

        rendimiento = []

        lista_volatilidad = linspace_resultado

        for voaltilidad in lista_volatilidad:

            # Numero de acciones
            n_assets = df.shape[1]

            # Función objetivo: maximizar retorno anualizado
            def funcion_objetivo(pesos):
                retorno = np.mean(np.dot(df, pesos))
                
                return - (retorno * 252)

            # Restricción 1: suma de los pesos == 1
            restriccion_suma = {'type': 'eq', 'fun': lambda pesos: np.sum(pesos) - 1}

            # Restricción 2: volatilidad anualizada == umbral
            umbral_volatilidad = voaltilidad
            restriccion_vol = {
                'type': 'eq',
                'fun': lambda pesos: (np.std(np.dot(df, pesos)) * np.sqrt(252)) - umbral_volatilidad
            }

            # Límites para los pesos
            boundaries = [(0, 1) for _ in range(n_assets)]

            # Pesos iniciales iguales
            pesos_iniciales = np.array([1 / n_assets] * n_assets)

            # Optimización
            resultado = minimize(
                funcion_objetivo,
                pesos_iniciales,
                method='SLSQP',
                bounds=boundaries,
                constraints=[restriccion_suma, restriccion_vol]
            )
            rendimiento.append(-resultado.fun)

        return rendimiento 
    
    def sharpe_ratio(self, df: pd.DataFrame) -> list:
        
        # Activo libre de riesgo
        Rf = 10

        #Numero de activos
        n_assets = df.shape[1]

        # Función objetivo: maximizar retorno anualizado
        def funcion_objetivo(pesos):

            Rentabilidad_Anualizada = np.mean(np.dot(df, pesos)) * 252
            volatilidad_anualizada = np.std(np.dot(df, pesos)) * np.sqrt(252)
            
            return - ((Rentabilidad_Anualizada - Rf) / volatilidad_anualizada)

        # Restricción 1: suma de los pesos == 1
        restriccion_suma = {'type': 'eq', 'fun': lambda pesos: np.sum(pesos) - 1}

        # Límites para los pesos
        boundaries = [(0, 1) for _ in range(n_assets)]

        # Pesos iniciales iguales
        pesos_iniciales = np.array([1 / n_assets] * n_assets)

        # Optimización
        resultado = minimize(
            funcion_objetivo,
            pesos_iniciales,
            method='SLSQP',
            bounds=boundaries,
            constraints=[restriccion_suma]
        )
        print(f"Pesos óptimos {resultado.x}")
        print(f"ratio de Sharpe {-resultado.fun}")

        lista_pesos_nuevos = resultado.x
        rentabilidad_portafolio = np.mean(np.dot(df, lista_pesos_nuevos)) * 252
        volatilidad_portafolio = np.std(np.dot(df, lista_pesos_nuevos)) * np.sqrt(252)

        # print(rentabilidad_portafolio)
        # print(volatilidad_portafolio)


        return -resultado.fun, resultado.x, rentabilidad_portafolio, volatilidad_portafolio
    


    
    def grafico_frontera_eficiente_CML(self, df: pd.DataFrame, linspace_resultado: list, rf: float, sharpe_ratio: float):
        """
        Dibuja la frontera eficiente y la línea de tangencia (CAL).
        
        Args:
            df (pd.DataFrame): Datos históricos de rendimientos.
            linspace_resultado (list): Lista de volatilidades objetivo.
            rf (float): Tasa libre de riesgo.
            sharpe_ratio (float): Ratio de Sharpe del portafolio óptimo.
        """

        lista_rendimiento = self.maxifrontera(df, linspace_resultado)
        lista_volatilidad = linspace_resultado

        df_frontera = pd.DataFrame({
            'Rentabilidad Anual': lista_rendimiento,
            'Volatilidad Anual': lista_volatilidad,
        })

        sns.set(style="whitegrid", context="notebook")
        plt.figure(figsize=(12, 7))

        # ➤ Portafolios: puntos azules pequeños
        sns.scatterplot(
            x='Volatilidad Anual',
            y='Rentabilidad Anual',
            data=df_frontera,
            color='blue',
            s=30,
            label='Portafolios',
            edgecolor='black'
        )

        # ➤ Frontera eficiente: línea negra, delgada y discontinua
        sns.lineplot(
            x='Volatilidad Anual',
            y='Rentabilidad Anual',
            data=df_frontera,
            color='black',
            linewidth=1,
            linestyle='--',
            label='Frontera Eficiente'
        )

        # ➤ Línea de Tangencia (CAL): roja, delgada
        x_vals = np.linspace(0, df_frontera['Volatilidad Anual'].max(), 100)
        y_vals = rf + sharpe_ratio * x_vals
        plt.plot(
            x_vals,
            y_vals,
            color='red',
            linestyle='--',
            linewidth=1,
            label='Línea de Tangencia (CAL)'
        )

        # ➤ Estética
        plt.title('Frontera Eficiente del Portafolio - CAL', fontsize=16, fontweight='bold')
        plt.xlabel('Volatilidad Anual', fontsize=12)
        plt.ylabel('Rentabilidad Anual', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def portafolio_final(self, lista_rentabilidad: list, lista_volatilidad: list,coeficiente_aversion: float) -> list:
        

        n_assets = 2

        # Función objetivo: Maximizar utilidad
        def funcion_objetivo(pesos):

            Rentabilidad_Anualizada = np.dot(lista_rentabilidad, pesos)
            volatilidad_anualizada = np.dot(lista_volatilidad, pesos)
            
            return - (Rentabilidad_Anualizada - ((coeficiente_aversion / 2) * volatilidad_anualizada ** 2))

        # Restricción 1: suma de los pesos == 1
        restriccion_suma = {'type': 'eq', 'fun': lambda pesos: np.sum(pesos) - 1}

        # Límites para los pesos
        boundaries = [(0, 1) for _ in range(n_assets)]

        # Pesos iniciales iguales
        pesos_iniciales = np.array([1 / n_assets] * n_assets)

        # Optimización
        resultado = minimize(
            funcion_objetivo,
            pesos_iniciales,
            method='SLSQP',
            bounds=boundaries,
            constraints=[restriccion_suma]
        )

        lista_pesos_nuevos = resultado.x
        rentabilidad_portafolio = np.dot(lista_rentabilidad, lista_pesos_nuevos)
        volatilidad_portafolio = np.dot(lista_volatilidad, lista_pesos_nuevos)
        print(f"Rentabilidad portafolio final {rentabilidad_portafolio}")
        print(f"Volatilidad portafolio final {volatilidad_portafolio}")

        print(f"Tolerancia al riesgo {(1 / coeficiente_aversion)}%")

        print(f"Pesos portafolio final {resultado.x}")
        print(f"Utilidad maximizada {-resultado.fun}")
