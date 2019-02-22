# -*- coding: utf-8 -*-
"""
Implementacion tarea 1.2

@author: Daniela Blanco
"""

import matplotlib.pyplot as plt

"""
1.3. Another module/script should be able to look at the data and detect anomalies. 
We can define these as points which are very "atypical" from other points in the data. 
The threshold over which a point is “atypical” should be configurable and something which you 
have to decide.  Feel free to use any algorithm of your choice to tag points as outliers. 

The anomalies should be printed, plotted or presented in some other way that is considered 
appropriate.
"""

data = pd.read_csv('F:/muttdata/desafio/serie_BTC_CNY.csv')
data = data.set_index('date')

data[['open_cny', 'high_cny', 'low_cny', 'close_cny']].boxplot()
plt.title('Bloxplot - CNY')

data[['open_usd', 'high_usd', 'low_usd', 'close_usd']].boxplot()
plt.title('Bloxplot - USD')
