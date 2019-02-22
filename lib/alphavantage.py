# -*- coding: utf-8 -*-
"""
Interacccion con Api alphavantage

@author: Daniela Blanco
"""
import requests 
import pandas as pd

class AlphaVantage:
    API_URL = "https://www.alphavantage.co/query?"
    
    def __init__(self, api_key):
        """
        Parametros:
            api_key: key para conexion api            
        """
        self.apiKey = api_key

    def obtenerSerieDiariaMoneda(self, moneda, mercado, fecha_inicio, fecha_fin):
        """
        Obtiene datos via request HTTP, formato JSON
        Filtra segun fechas inicio y fin
        
        Parametros:
            moneda:  str, tipos disponibles en https://www.alphavantage.co/digital_currency_list/
            mercado: str, tipos disponibles en https://www.alphavantage.co/physical_currency_list/
            fecha_inicio: date formato YYYY-MM-DD, filtra desde esta fecha
            fecha_fin: date formato YYYY-MM-DD, filtra hasta esta fecha
            
        Salida:
            pandas: serie obtenida y filtrada
            
            Si no: False
        """
        
        data = {
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": moneda,
                "market": mercado,
                "datatype": 'json',
                "apikey": self.apiKey,
        }
        respuesta = requests.get(AlphaVantage.API_URL, params=data)
        
        if respuesta.status_code == requests.codes.ok:
            json = respuesta.json()

            # solo serie
            serie = json["Time Series (Digital Currency Daily)"]
            pd_serie = pd.DataFrame.from_dict(serie, orient='index')

            # filtro
            pd_serie_filtrado = pd_serie.loc[fecha_inicio:fecha_fin]
            
            return pd_serie_filtrado
            
        else:
            return False

    def guardaSerieDiariaMonedaCsv(self, serie, archivo):
        """
        Gaurda serie en archivo formato csv
        
        Parametros:
            serie:  obj pandas para exportar
            archivo: nombre del csv
            
        Salida:
            guarda csv en archivo
        """

        # tuneo columnas
        serie.reset_index(level=0,inplace=True)
        headers = ['date', 'open_cny', 'open_usd', 'high_cny', 'high_usd', 'low_cny', 'low_usd', 'close_cny', 'close_usd', 'volume', 'market_cap_usd']
        serie.columns = headers
        
        serie.to_csv(archivo, sep=',', encoding='utf-8', index=False)
