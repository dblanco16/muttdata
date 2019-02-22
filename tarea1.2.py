# -*- coding: utf-8 -*-
"""
Implementacion tarea 1.2

@author: Daniela Blanco
"""

import matplotlib.pyplot as plt


"""
1.2 Create a second Python script that reads the output file(s) from point ( 1 ) and 
plots the open and close prices of a given symbol, for the last 30 days. 
This script should also print the average difference between the open and closing price 
(the price range) for all of those 30 days.
"""

data = pd.read_csv('serie_BTC_CNY.csv')
data['rango_cny'] = (data['close_cny'] + data['open_cny']) / 2
data['rango_usd'] = (data['close_usd'] + data['open_usd']) / 2

data[["date", "open_cny", "close_cny", "rango_cny"]].plot(x="date", kind="line")
plt.title('Enero 2019 - Valores apertura, cierre y rango en CNY')
plt.show()

data[["date", "open_usd", "close_usd", "rango_usd"]].plot(x="date", kind="line")
plt.title('Enero 2019 - Valores apertura, cierre y rango en USD')
plt.show()
