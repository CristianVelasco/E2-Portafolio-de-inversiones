# Standard library imports
import os
import warnings

# Third party imports
import yfinance as yf
import pandas as pd
import numpy as np
import time


class YfinanceETL:

    def __init__(self):
        pass

    def extractionyfinance(self, symbols: list, date: str) -> pd.DataFrame: 

        """Extracción de los valores que queremos en nuestro portafolio apartir de una fecha establecida
        
        Args:
            symbols (list) : Lista de simbolos de la empresa listada en bolsa
            Date (str) : Fecha de obtención de los valores de la acción 

        Return: 

            pd.Dataframe : Datafrmae de los valores de la acción, Fecha, valor, simbolo etc. 
        
        """

        # symbols = ['EC', 'CIB', 'AVAL', 'CMSA', 'NU', 'ICAP'] # Valores por defecto

        symbols = symbols

        # start_date = '2021-12-29' # Valores por defecto

        start_date = date

        dataframes = {}


        for symbol in symbols:
            print(f"Descargando datos de: {symbol}")
            
            try:
                ticker = yf.Ticker(symbol)

                hist = ticker.history(start=start_date)  
                
                if hist.empty:
                    print(f" No hay datos disponibles para: {symbol}")
                    continue

                hist['Symbol'] = symbol
                dataframes[symbol] = hist

                time.sleep(1)

            except Exception as e:
                print(f"Error al descargar {symbol}: {e}")

        if dataframes:
            df_acciones = pd.concat(dataframes.values())
        else:
            print(" No se pudo descargar ningún dato.")

        return df_acciones
    


    def transformationyfinance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transformación del dataframe extraído a dataframe de rendimientos diarios porcentuales.
        """
        df = df.reset_index()

        # Obtención de valores de cierre de las acciones
        df_pivot = df.pivot_table(values='Close', index='Date', columns='Symbol')
        df_pivot.reset_index(inplace=True)

        # Dada la existencia de valores vacíos, interpolo entre t-1 y t + 1. Manejo de missing values
        df_pivot.iloc[:, :] = df_pivot.interpolate(method='linear', limit_direction='both')

        df_transformado = df_pivot

        df_transformado['Date'] = pd.to_datetime(df_transformado['Date'])
        df_transformado.set_index('Date', inplace=True)

        # Cálculo de rendimientos logarítmicos
        df_rendimientos = np.log(df_transformado / df_transformado.shift(1)) * 100

        # Renombrado de columnas de rendimientos
        df_rendimientos.columns = [f"{col}_Rendimiento" for col in df_rendimientos.columns]

        # Unión de columnas de rendimientos y valores de cierre de la acción
        df_portafolio = pd.concat([df_transformado, df_rendimientos], axis=1).reset_index()

        return df_portafolio



    # def transformationyfinance_2(self, df: pd.DataFrame) -> pd.DataFrame:

    #     """
    #     Este metodo retorna el rendimiento del portafolio con pesos iniciales arbitrarios

    #     Args:
    #         df (pd.Dataframe) : Dataframe con los valores de cierre y rendimientos logaritmicos calculados
    #         w (list) : lista de pesos arbitrarios. 

    #     Return: 

    #         pd.Dataframe : Retorna un dataframe con los rendimientos y volatilidades 
    #         diarias y anualizadas para las accion y el portafolio 

    #     """
    #     df_rend = df.filter(like='Rendimiento')
    #     df_rend = df_rend.iloc[1:].reset_index(drop=True)
    #     n_assets = df_rend.shape[1]

    #     w = np.array([1 / n_assets] * n_assets)

    #     #Producto punto acciones vs pesos arbitrarios
    #     df_portafolio  = df_rend.values.dot(w)

    #     df_rend['Portafolio'] = df_portafolio

    #     promedio_diario = df_rend.mean()
    #     promedio_anual = df_rend * 252

    #     desv_std_diaria = df_rend.std()
    #     desv_std_anual = df_rend * np.sqrt(252)

    #     # df_portafolio_resume = pd.DataFrame({
    #     #     'Valores': [
    #     #         promedio_diario,
    #     #         promedio_anual,
    #     #         desv_std_diaria,
    #     #         desv_std_anual
    #     #     ]
    #     # }, index=[
    #     #     'Rentabilidad Diaria',
    #     #     'Rentabilidad Anual',
    #     #     'Volatilidad Diaria',
    #     #     'Volatilidad Anual'
    #     # ])

    #     df_portafolio_resume = pd.DataFrame({
    #         'Rentabilidad Diaria': promedio_diario,
    #         'Rentabilidad Anual': promedio_anual,
    #         'Volatilidad Diaria': desv_std_diaria,
    #         'Volatilidad Anual': desv_std_anual
    #     }).T 

    #     print(df_portafolio_resume)
    #     return df_portafolio_resume
    
    # def transformationyfinance_2(self, df: pd.DataFrame) -> pd.DataFrame:

    #     """
    #     Este metodo retorna el rendimiento del portafolio con pesos iniciales distribuidos igualmente

    #     Args:
    #         df (pd.Dataframe) : Dataframe con los valores de cierre y rendimientos logaritmicos calculados

    #     Return: 
    #         pd.DataFrame : Retorna un dataframe con los rendimientos y volatilidades 
    #         diarias y anualizadas para las acciones y el portafolio 
    #     """

    #     df_rend = df.filter(like='Rendimiento')
    #     df_rend = df_rend.iloc[1:].reset_index(drop=True) 
        
    #     #Numero de activos
    #     n_assets = df_rend.shape[1]

    #     # pesos iguales
    #     w = np.array([1 / n_assets] * n_assets)  

    #     df_portafolio = df_rend.values.dot(w)
    #     df_rend['Portafolio'] = df_portafolio

    #     # Calcular estadísticas
    #     promedio_diario = df_rend.mean()
    #     promedio_anual = promedio_diario * 252

    #     desv_std_diaria = df_rend.std()
    #     desv_std_anual = desv_std_diaria * np.sqrt(252)

        
    #     df_portafolio_resume = pd.DataFrame({
    #         'Rentabilidad Diaria': promedio_diario,
    #         'Rentabilidad Anual': promedio_anual,
    #         'Volatilidad Diaria': desv_std_diaria,
    #         'Volatilidad Anual': desv_std_anual
    #     }).T 

    #     print("\nResumen del Portafolio (incluye activos y portafolio):\n")
    #     print(df_portafolio_resume.round(6))

    #     return df_portafolio_resume

    
    
    def save_df_to_csv(self, df: pd.DataFrame, path: str, file_name: str):
        
        """Este metodo guarda un dataframe a un CSV file"""
 
        file_path = os.path.join(path, file_name)
        
        df.to_csv(file_path, index=False)

    def run(self, symbols: list, date: str, data_path_processed: str, date_last: str):


        df_inicial = self.extractionyfinance(symbols, date)

        df_transformado = self.transformationyfinance(df_inicial)

        self.save_df_to_csv(
            df_transformado, data_path_processed, f"Portafolio_{date_last}.csv"
        )