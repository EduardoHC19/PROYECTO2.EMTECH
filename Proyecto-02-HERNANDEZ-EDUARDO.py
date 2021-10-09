# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:32:13 2021

@author: eduar
"""

import numpy as np
import pandas as pd
import seaborn as sns
import csv
import matplotlib.pyplot as plt

# Abrimos el archivo, especificando la ruta y usando pd.read_csv()
synergyFile = 'synergy_logistics_database.csv'
df = pd.read_csv(synergyFile, index_col='register_id')

#Podemos comenzar a agrupar por transport_mode, para este ejercicio vamos a 
#sacar cuenta de cuantos envíos hay por categoría:
transp_mode_count = df['transport_mode'].value_counts()
print(transp_mode_count)

#Para algo más interesante grafiquemos ahora la ganancia promedio de estas 
#categorías de transporte:
prom_val_transp = df.groupby('transport_mode')['total_value'].mean()



'''***************************************************************************
1- Rutas de importación y exportación
******************************************************************************'''
rutasUnicas = df[['direction', 'origin', 'destination', 'transport_mode', 'total_value']]
rutasConteoDF = rutasUnicas.groupby(['direction', 'origin', 'destination', 'transport_mode']).sum()
rutasConteoDF = rutasConteoDF.sort_values(by = 'total_value', ascending = False) 

#Separarlos por exportaciones e importaciones:
top10exp = rutasConteoDF.xs('Exports').head(10)
top10imp = rutasConteoDF.xs('Imports').head(10)


#Graficación de resultados en gráficas de barras.Se tienen que generar la
#etiqueta para el eje x. Se agrega en el DataFrame creado.
top10exp['xlabel'] = top10exp.index.to_list()
top10imp['xlabel'] = top10imp.index.to_list()

#------------Se genera la gráfica de barras para las exportaciones-------------
sns.set(rc = {"figure.figsize": (18, 6)}) #width = 18, height = 6
sns.barplot(data = top10exp, x = 'xlabel', y = 'total_value')

#specify axis labels
plt.xlabel('Paises', size=20, weight=900)
plt.xticks(ticks=range(len(top10exp)), labels=top10exp.xlabel, rotation=90)
plt.tick_params(axis ='both', labelsize = 16)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Mejores Rutas de Exportación', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------

#------------Se genera la gráfica de barras para las importaciones-------------
sns.set(rc = {"figure.figsize": (18, 6)}) #width = 18, height = 6
sns.barplot(data = top10imp, x = 'xlabel', y = 'total_value')

#specify axis labels
plt.xlabel('Paises', size=20, weight=900)
plt.xticks(ticks=range(len(top10imp)), labels=top10imp.xlabel, rotation=90)
plt.tick_params(axis ='both', labelsize = 16)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Mejores Rutas de Importación', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------





'''***************************************************************************
2- Medio de transporte utilizado (son solo 4 medios de transporte)
******************************************************************************'''
medioTransp = df[['direction', 'transport_mode', 'total_value']]
medioTranspDF = medioTransp.groupby(['direction', 'transport_mode']).sum()
medioTranspDF = medioTranspDF.sort_values(by = 'total_value', ascending = False) 

#Separarlos por exportaciones e importaciones:
topTransp_exp = medioTranspDF.xs('Exports').head(4)
topTransp_inp = medioTranspDF.xs('Imports').head(4)

#Graficación de resultados en gráficas de barras. Se tienen que generar la
#etiqueta para el eje x. Se agrega en el DataFrame creado.
topTransp_exp['xlabel'] = topTransp_exp.index.to_list()
topTransp_inp['xlabel'] = topTransp_inp.index.to_list()

#------------Se genera la gráfica de barras para las exportaciones-------------
sns.set(rc = {"figure.figsize": (18, 6)}) #width = 18, height = 6
sns.barplot(data = topTransp_exp, x = 'xlabel', y = 'total_value')

#specify axis labels
plt.xlabel('Medio de Transporte', size=20, weight=900)
plt.tick_params(axis ='both', labelsize = 18)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Medio de Transporte para Exportaciones', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------

#------------Se genera la gráfica de barras para las importaciones-------------
sns.set(rc = {"figure.figsize": (18, 6)}) #width = 18, height = 6
sns.barplot(data = topTransp_inp, x = 'xlabel', y = 'total_value')

#specify axis labels
plt.xlabel('Medio de Transporte', size=20, weight=900)
plt.tick_params(axis ='both', labelsize = 18)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Medio de Transporte para Importaciones', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------




'''***************************************************************************
3- Valor total de importaciones y exportaciones
******************************************************************************'''
#Se calcula el total de las importaciones y exportaciones, sin tomar en cuenta
#direcciones, origen,...
imp_ExpTotal = df[['direction', 'total_value']]
imp_ExpTotalDF = imp_ExpTotal.groupby(['direction']).sum()
expo_total = int(imp_ExpTotalDF.values[0])
imp_total = int(imp_ExpTotalDF.values[1])

#Se separan las rutas de envios de acuerdo a si se trata de importaciones o 
#exportaciones.
imp_Exp = df[['direction', 'origin', 'destination', 'total_value']]
imp_ExpDF = imp_Exp.groupby(['direction', 'origin', 'destination']).sum()
imp_ExpDF = imp_ExpDF.sort_values(by = 'total_value', ascending = False) 

#Separarlos por exportaciones e importaciones:
expDF = imp_ExpDF.xs('Exports')
impDF = imp_ExpDF.xs('Imports')

#Se considera solamente el pais de origen tratarse de exportaciones, , el de 
#destino puede ser ignorado.
expDF = expDF.groupby(['origin']).sum()
expDF = expDF.sort_values(by = 'total_value', ascending = False) 

#Se agrega una columna con la suma acumulada de exportaciones.
expDF['cumulative'] = expDF.values.cumsum()
expDF['xlabel'] = expDF.index.to_list()



#Al tratarse de importaciones, se considera solamente el pais de destino, el de 
#origen puede ser ignorado.
impDF = impDF.groupby(['destination']).sum()
impDF = impDF.sort_values(by = 'total_value', ascending = False) 

#Se agrega una columna con la suma acumulada de importaciones y otra para los índices.
impDF['cumulative'] = impDF.values.cumsum()
impDF['xlabel'] = impDF.index.to_list()



#------------Se grafican los resultados acumulados de exportaciones------------
sns.set(rc = {"figure.figsize": (12, 8)}) #width = 18, height = 6
sns.barplot(data = expDF, x = 'xlabel', y = 'cumulative')

#Graficando el indicador del 80%.
temp = np.repeat(expo_total*0.8, len(expDF))
plt.plot(expDF.xlabel, temp, 'k--', linewidth = 4)

#specify axis labels
plt.xlabel('Paises', size=20, weight=900)
plt.xticks(ticks=range(len(expDF)), labels=expDF.xlabel, rotation=90)
plt.tick_params(axis ='both', labelsize = 16)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Exportaciones Acumuladas', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------

#------------Se grafican los resultados acumulados de importaciones------------
sns.set(rc = {"figure.figsize": (12, 8)}) #width = 18, height = 6
sns.barplot(data = impDF, x = 'xlabel', y = 'cumulative')

#Graficando el indicador del 80%.
temp = np.repeat(imp_total*0.8, len(impDF))
plt.plot(impDF.xlabel, temp, 'k--', linewidth = 4)

#specify axis labels
plt.xlabel('Paises', size=20, weight=900)
plt.xticks(ticks=range(len(impDF)), labels=impDF.xlabel, rotation=90)
plt.tick_params(axis ='both', labelsize = 16)
plt.ylabel('Valor Total', size=20, weight=900)
plt.title('Importaciones Acumuladas', size=22, weight=600)

#display barplot
plt.show()
#-----------------------------------------------------------------------------









