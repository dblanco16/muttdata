# -*- coding: utf-8 -*-
"""
Implementacion tarea 3 - Economics meets Data Science

@author: Daniela Blanco
"""

import pandas as pd
import numpy as np

# YEAR	Año	
# NUI	Número único que identifica un establecimiento	
# CIIU3	Ciiu-Rev 3	Código	Industry id
# REGION
# FORPRO Forma de propiedad	
# FABVAL	Ventas de productos fabricados 	Miles de pesos
# EXPVAL	Valor productos exportados	Miles de pesos
# VA	Valor Agregado	Miles de pesos
# EMPTOT	Total Promedio Ocupados Directos e Indirectos Año	Número de personas
# REMPAG	Remuneración Pagada	Miles de pesos
# VSTK	Valor Nominal del Stock de Capital Fijo	Miles de pesos

data = pd.read_csv('datos_ine.csv', na_values=['\\N'])
data = data.set_index('Obs')
data.dtypes


"""
1. Clean the dataset:
a. Remove the observations where the domestic sales or exports are either negative or 
missing (they appear as “.”) or where the total sales are null or negative.
"""

frec_nulos = data.isnull().sum()

data.loc[data['fabval'] <0]
data.loc[data['expval'] <0]

# => No hay nulos ni negativos para limpiar

"""
b. Filter the dataset in any other way you deem necessary. 
You should end with a balanced panel i.e the dataset should contain firms/companies that were seen 
in each unit of time (see https://en.wikipedia.org/wiki/Panel_data#Example for details). 
Hint: at some point you need to use a `group by`.
"""

frec_year = pd.crosstab(index=data["year"], columns="count")  
frec_ciiu3 = pd.crosstab(index=data["ciiu3"], columns="count")  
frec_region = pd.crosstab(index=data["region"], columns="count")  # 13 regiones, todas validas
frec_forpro = pd.crosstab(index=data["forpro"], columns="count")  # 6 regiones, dos no son validas

# se sacan las formas de propiedad invalidas
data_clean = data.loc[data['forpro'] != 0]
data_clean = data_clean.loc[data['forpro'] != 100]
frec_forpro_clean = pd.crosstab(index=data_clean["forpro"], columns="count")  # 6 regiones, dos no son validas

frec_year_region_clean = pd.crosstab(index=data_clean["year"], 
                             columns=[data_clean["region"]],
                             margins=True)

frec_year_region_clean

# genero panel con establecimientos balanceados por años
nui_cantidad_anios = data_clean.groupby(['nui']).agg({'year': 'count'})
nui_todos_anios =  nui_cantidad_anios.loc[nui_cantidad_anios['year'] == 6]

panel_balanceado =  data_clean.loc[nui_todos_anios.index]


"""
2. Define 4 types of firms: 
“Starter” if the firm doesn’t export in 2001 but does export in 2006; 
“Stopper” if the firm exports in 2001 but not in 2006; 
“Cont. Exporter” if the firm exports in 2001 and 2006;
“Cont. Non-Exporter” if the firm neither exports in 2001 nor 2006. 
Tag firms accordingly in your dataframe.
Create a table (or several) with the mean and median annual sales and employment growth rates for 
each firm.
"""

data_nui = data_clean['nui'].to_frame()
data_nui = data_nui.drop_duplicates('nui')

data_nui['type_firm'] = np.NaN

cond_not_exp_2001 =  data_clean.loc[(data_clean['year'] == 2001) & (data_clean['expval'] == 0)]['nui']
cond_exp_2006 =  data_clean.loc[(data_clean['year'] == 2006) & (data_clean['expval'] > 0)]['nui']
cond_not_exp_2006 =  data_clean.loc[(data_clean['year'] == 2006) & (data_clean['expval'] == 0)]['nui']
cond_exp_2001 =  data_clean.loc[(data_clean['year'] == 2001) & (data_clean['expval'] > 0)]['nui']

# starter
cond_starter = data_nui[data_nui['nui'].isin(cond_not_exp_2001)]['nui']
cond_starter = cond_starter[cond_starter.isin(cond_exp_2006)]

data_nui.loc[data_nui['nui'].isin(cond_starter), 'type_firm'] = 'Starter'

# stopper
cond_stopper = data_nui[data_nui['nui'].isin(cond_not_exp_2006)]['nui']
cond_stopper = cond_stopper[cond_stopper.isin(cond_exp_2001)]

data_nui.loc[data_nui['nui'].isin(cond_stopper), 'type_firm'] = 'Stopper'

# Cont. Exporter
cond_exporter = data_nui[data_nui['nui'].isin(cond_exp_2006)]['nui']
cond_exporter = cond_exporter[cond_exporter.isin(cond_exp_2001)]

data_nui.loc[data_nui['nui'].isin(cond_exporter), 'type_firm'] = 'Cont. Exporter'

# Cont. Non-Exporter
cond_no_exporter = data_nui[data_nui['nui'].isin(cond_not_exp_2001)]['nui']
cond_no_exporter = cond_no_exporter[cond_no_exporter.isin(cond_not_exp_2006)]

data_nui.loc[data_nui['nui'].isin(cond_no_exporter), 'type_firm'] = 'Cont. Non-Exporter'

frec_nulos = data_nui.isnull().sum()
frec_nulos

frec_type_firm = pd.crosstab(index=data_nui["type_firm"], columns="count")
frec_type_firm

data_clean_type_firm = pd.merge(data_clean, data_nui, on='nui')

# tablas FABVAL
tabla_fabval_mean = data_clean_type_firm.groupby(['year','type_firm']).agg({'fabval': 'mean'})
tabla_fabval_mean
tabla_fabval_median = data_clean_type_firm.groupby(['year','type_firm']).agg({'fabval': 'median'})
tabla_fabval_median

# tablas EMPTOT
tabla_emptot_mean = data_clean_type_firm.groupby(['year','type_firm']).agg({'emptot': 'mean'})
tabla_emptot_mean
tabla_emptot_median = data_clean_type_firm.groupby(['year','type_firm']).agg({'emptot': 'median'})
tabla_emptot_median

"""
[HARD]: Survival rates 
Select only firms that did not engage in exporting in 2001 but did in 2002 (a.k.a the “new exporters”). 


Using the subset of firms obtained in the previous point, compute and plot the share of exporting plants of a given exporting age that continue to export in the following period for firms in the period 2003-2006 (this is known as the survival rate). 
What we mean by this is that if the firm exported in 2002 and continues to export in 2003 then its exporting age is 1, if it continues to export in 2004 then its exporting age is 2 and so on. Therefore the idea is to plot exporting age against survival rate. 
What is the probability of remaining in the export market for plants that have been exporting for only one year? For three years?  
What can you say about this? Hint: run regressions of the form: $I_it = beta * I_it-1 + e_it$ where $I_it$ is equal to 1 if plant i is exporting at age t and equal to 0 otherwise and e_it is the error term of the regression.

Hint: in order to relate year with age, take into account the definition of the subset.


Bonus!
If you have time, run any analysis you would like over the data. You can find some fun suggestions below:
https://erikbern.com/2017/05/23/conversion-rates-you-are-most-likely-computing-them-wrong.html
https://gist.github.com/chandinijain/a91cb0c8a49e7ef4885e03ab7c247994
"""