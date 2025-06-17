import os
import warnings

# Third party imports
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
from scipy.optimize import minimize

# Local application imports

from etl_yahoo import YfinanceETL
# from numerical_methods import FronteraEficiente, Sharperatio
from numerical_methods import Sharperatio


path_processed = rf'your\path'


# Acciones que se analizaran en el portafolio
symbols = ['EC', 'AVAL', 'CMSA', 'NU', 'ICAP'] 

#Inicio de consulta fechas de api
start_date = '2023-12-29' 
fecha_hoy = datetime.today().strftime('%Y-%m-%d')


#Activo libre de riesgo
rf = 10

# Coeficiente de aversión [1 /Coeficiente de aversión] % cuanto de mi capital estoy dispuesto a perder en una inversión a riesgo
coeficiente_aversion = 0.05

def etl(symbols: list, date: str, data_path_processed: str, date_last: str):

    """Este metodo
    Args:

    Returns:
        None"""
    
    df_extrac = YfinanceETL()
    
    df_extrac.run(symbols = symbols , date = start_date, data_path_processed = path_processed , date_last = fecha_hoy)



# def frontera_eficiente(data_path_processed: str, date_last: str):

#     forntera = FronteraEficiente()

#     df_portafolio = forntera.load_df_portafolio(path_processed=data_path_processed, date_last=date_last)

#     df_portafolio_2 = forntera.transformationyfinance_2(df_portafolio)

#     lista_rendimientos = forntera.list_volatilidad(df_portafolio_2)

#     forntera.maxifrontera(df_portafolio, linspace_resultado=lista_rendimientos)

#     forntera.grafico_frontera_eficiente(df_portafolio,lista_rendimientos)


def ratio_sharpe(data_path_processed: str, date_last: str):

    sharperatio = Sharperatio()

    df_portafolio = sharperatio.load_df_portafolio(path_processed=data_path_processed, date_last=date_last)

    df_portafolio_2 = sharperatio.transformationyfinance_2(df_portafolio)

    lista_rendimientos = sharperatio.list_volatilidad(df_portafolio_2)

    sr, pesos_optimo, rentabilidad, volatilidad  = sharperatio.sharpe_ratio(df_portafolio)

    lista_rentabilidad = [rentabilidad,rf]

    lista_volatilidad = [volatilidad,0]

    sharperatio.grafico_frontera_eficiente_CML(df_portafolio, lista_rendimientos, rf ,sr)

    sharperatio.portafolio_final(lista_rentabilidad, lista_volatilidad, coeficiente_aversion) 




def main_flow():
    
    etl(symbols = symbols , date = start_date, data_path_processed = path_processed , date_last = fecha_hoy)

    # frontera_eficiente(data_path_processed = path_processed , date_last = fecha_hoy)

    ratio_sharpe(data_path_processed = path_processed , date_last = fecha_hoy)

main_flow()