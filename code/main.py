import streamlit as sl
import funciones
import pandas as pd
import numpy as np
from st_aggrid import AgGrid


tercios=('20','25','32','40','50','63','80','100','125','160','200','250','315','400','500','630','800','1.0k','1.25k','1.6k','2.0k','2.5k','3.15k','4.0k','5.0k','6.3k','8.0k','10k','12.5k','16k','20k')
octavas=('32','63','125','250','500','1.0k','2.0k','4.0k','8.0k','16k')

# COMIENZA LA WEB
sl.write("# Room Acoustics Program - R.A.P.")
sl.write("##### ¿Quién necesita un Excel para hacer Acústica?")
sl.write("#### Para comenzar, sube un archivo '.csv' con los datos en filas (tercios o banda completa) o rellena la tabla que encontrarás abajo.")

#subir archivo
archivo=sl.file_uploader("Fichero con los datos.", 'csv')
modo=tercoctava=sl.checkbox('1/3 de octava')

with sl.sidebar:
    sl.write("### Selecciona el cálculo que quieras hacer")

    option = sl.radio(
        '¿Qué cálculo quieres hacer?',
        ('Nada, sólo estoy mirando','Diferencia de niveles', 'Diferencia de niveles normalizada','Diferencia de niveles estandarizada','Indice de reduccion sonora')
    )
    option2 = sl.radio(
        '¿Quieres calcular un valor absoluto?',
        ('No','Valor global', 'Valor global ponderado A','Valor global para ruido aereo')
    )

# Condiciones Checkbox
if tercoctava:
    df=pd.DataFrame(
        np.zeros((2,31)),
        columns=tercios,

    )
else:
    df=pd.DataFrame(
        np.zeros((2,10)),
        columns=octavas,

    )

# Condiciones subida archivo
if archivo is not None:
    datos=pd.read_csv(archivo)
    (y,x)=datos.shape
    if x==10:
        df=pd.DataFrame(
            datos.values,
            columns=octavas
        )

    elif x==31:
        df=pd.DataFrame(
            datos.values,
            columns=tercios
        )
grid_return = AgGrid(df, editable=True)
new_df = grid_return['data']

# Selección de cálculos

area= sl.number_input('Area de absorción sonora')
rt=sl.number_input('Tiempo de reverberación en la sala receptora')
superficie=sl.number_input('Superficie sobre la que se produce la transmisión directa')
if option=='Diferencia de niveles':
    d=funciones.levelDifference(new_df.loc[0], new_df.loc[1])
elif option=='Diferencia de niveles normalizada':
    a=funciones.levelDifference(new_df.loc[0], new_df.loc[1])
    d=funciones.levelDifferenceNorm(a,area)
elif option=='Diferencia de niveles estandarizada':
    a=funciones.levelDifference(new_df.loc[0], new_df.loc[1])
    d=funciones.levelDifferenceSta(a,rt)
elif option=='Indice de reduccion sonora':
    a=funciones.levelDifference(new_df.loc[0], new_df.loc[1])
    d=funciones.indexReduction(a,superficie,area)
else:
    if modo==False:
        d=np.zeros((10))
    else:
        d=np.zeros((31))

#Mostrar resultados
if modo==False:
    fin=pd.DataFrame(columns=octavas)
else:
    fin=pd.DataFrame(columns=tercios)
fin.loc[0]=d
sl.dataframe(fin)

# Selección de valores globales

if option2=='Valor global':
    valorGlobal=funciones.obtainGlobal(d)
    valorGlobalFinal=sl.metric(label="Valor global", value=str(valorGlobal)+" dB")
elif option2=='Valor global ponderado A':
    valorGlobal=funciones.globalIndexA(fin,modo)
    valorGlobalFinal=sl.metric(label="Valor global", value=str(valorGlobal)+" dBA")
elif option2=='Valor global para ruido aereo':
    valorGlobal=funciones.globalValueAereo(fin,modo)
    valorGlobalFinal=sl.metric(label="Valor global", value=str(valorGlobal)+" dB")
else:
    valorGlobal=0



