# -*- coding: utf-8 -*-
"""
Implementacion tarea 1.1

@author: Daniela Blanco
"""
# spyder no toma bien el import
#import sys
#sys.path.insert(0, 'F:/muttdata/desafio/')
import lib.alphavantage as av

"""
1. Create a Python script that downloads the daily data from DIGITAL_CURRENCY_DAILY endpoint and 
stores it in a local file. 
Save the data in whichever file-format you judge best for your problem.
The script should take arguments to download data for a specified currency and for a time window. 

"""

# obtiene datos
api_key = 'JDLNYJZR454EMHNS'        
api = av.AlphaVantage(api_key)

moneda = 'BTC'
mercado = 'CNY'
fecha_inicio = '2019-01-01'
fecha_fin = '2019-01-31'

serie_filtrada = api.obtenerSerieDiariaMoneda(moneda, mercado, fecha_inicio, fecha_fin)

# guarda csv
archivo_salida = 'serie_'+moneda+'_'+mercado+'.csv'
api.guardaSerieDiariaMonedaCsv(serie_filtrada, archivo_salida)