import math

# Función que calcula la diferencia de niveles entre utilizando dos arrays de datos
# l1: Niveles registrados en la sala emisora
# l2: Niveles registrados en la sala receptora
# Nota: l1 y l2 tienen que tener el mismo número de datos
def levelDifference(l1, l2):
    if (len(l1)!=len(l2)):
        print("L1 y L2 deben tener el mismo número de valores")
    else:
        d=[0]*len(l1)
        for i in range(0,len(l1)):
            d[i]=l1[i]-l2[i]
        return d
    
# Función que calcula la diferencia de nvieles normalizada
# dl: diferencia de niveles ya calculada (ver levelDifference)
# a: área de absorción sonora
def levelDifferenceNorm(dl,a):
    dn=[0]*len(dl)
    for i in range(0,len(dl)):
        dn[i]=dl[i]-10*math.log10(a/10)
    return dn

# Función que calcula la diferencia de niveles estandarizada
# dl: diferencia de niveles ya calculada (ver levelDifference)
# rt: tiempo de reverberación en la sala receptora
def levelDifferenceSta(dl,rt):
    ds=[0]*len(dl)
    for i in range(0,len(dl)):
        ds[i]=dl[i]-10*math.log10(rt/0.5)
    return ds

# Función que calcula el índice de reducción sonora aparente
# dl: diferencia de niveles ya calculada (ver levelDifference)
# s: superficie sobre la que se produce la transmisión directa
# a: area de absorción sonora
def indexReduction(dl,s,a):
    ri=[0]*len(dl)
    for i in range(0,len(dl)):
        ri[i]=dl[i]-10*math.log10(s/a)
    return ri

# Función que calcula el valor global de determinado parámetro acústico
def obtainGlobal(x):
    suma=0
    for i in range(0, len(x)):
        suma=suma+10**(x[i]/10)    
    result=10*math.log10(suma)
    return result

# Función que calcular el índice global ponderado A
# x: índice a evaluar
# modo: variable que indica si se está en modo de tercio o de octava. 1=1/3octava, 0=octava
def globalIndexA(x,modo):
    if modo==False:
        correcciones=[-22.4,-14.9,-9.5,-6.3,-5.1,-5.3]
        d=x.iloc[0,2:8]
    else:
        d=x.iloc[0,7:25]
        correcciones=[-30.1,-27.1,-24.4,-21.9,-19.6,-17.6,-15.8,-14.2,-12.9,-11.8,-11.0,-10.4,-10.0,-9.8,-9.7,-9.8,-10.0,-10.5]

    valoresCorregidos=[0]*len(correcciones)
    suma=0
    for i in range(0,len(correcciones)):
        valoresCorregidos[i]=d.iloc[i]-correcciones[i]
        suma=suma+10**(valoresCorregidos[i]/10)
    return 10*math.log10(suma)

# Función que calcula el valor global para ruido aéreo
# x: diferencia de nivel o indice de reducción sonora en bandas de frecuencia
# modo: indica si las bandas son de 1/3 o de octava. 1=1/3octava, 0=octava
def globalValueAereo(x,modo):
    if modo==False:
        correcciones=[36.0,45.0,52.0,55.0,56.0,56.0]
        d=x.iloc[0,2:8]
    else:
        d=x.iloc[0,7:25]
        correcciones=[33.0,36.0,39.0,42.0,45.0,48.0,51.0,52.0,53.0,54.0,55.0,56.0,56.0,56.0,56.0,56.0,56.0,56.0]

    valoresCorregidos=[0]*len(correcciones)
    desvDesfa=2000
    contador=0
    while (desvDesfa>32.0):
        desvactual=0
        for i in range(0,len(correcciones)):
            valoresCorregidos[i]=correcciones[i]-(d.iloc[i]+contador)
            if valoresCorregidos[i]>0:
                desvactual=desvactual+valoresCorregidos[i]
        desvDesfa=desvactual
        contador=contador+1
    if modo==False:
        return correcciones[2]-contador
    elif modo==True:
        return correcciones[7]-contador
    
    
# Función que calcula el tiempo de reverberación de una sala estilo "caja de zapatos" utilizando la
# fórmula de Sabine.
# volumen: volumen de la sala
# superficie: superficie de todas las paredes con características absorbentes de la sala
# A: area de absorción sonora
def calculoSabine(volumen, A, superficie):
    t=0.16*volumen/(superficie*A)
    return t


# Función que calcula el area de absorción sonora, A.
# superficies: lista con las distintas superficies que contienen material absorbente en la sala
# alpha: lista con los coeficientes de absorción de cada superficie
def calculoAreaAbsorcion(superficies, alpha):
    if len(superficies)==len(alpha):
        A=0
        for x in superficies:
            temporal=supericies[x]*alpha[x]
            A=A+temporal
        return A
    else:
        print("superficies y alpha deben de tener la misma dimensión")
        return 0

# Función que calcula el tiempo de reverberación utilizando la fórmula de Eyring
# superficie:
def calculoEyring(superficies, alpha, volumen):
    if len(superficies)==len(alpha):
        A=0
        for x in superficies:
            temporal=superficies[x]*math.log(alpha[x])
            A=A+temporal
        tr=0.16*volumen/(-A)
        return tr
    else:
        print("superficies y alpha deben de tener las mismas dimensiones")
        return 0

             
