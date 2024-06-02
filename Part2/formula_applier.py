import numpy as np
import os
import io

os.chdir('C:/Users/Usuario/Documents/stage2_SAP_final_proj/wind_simulations')
lista_ficheros = []
for i, directory in enumerate(os.listdir()):
   if os.path.isdir(directory):
    for fichero in os.listdir(directory):
        if fichero.endswith('vel.asc'):
            lista_ficheros.append(os.path.join(directory, fichero))

valores_matriz = {}

for fichero in lista_ficheros:
    with open(fichero, 'r') as f:
        lines = f.readlines()
        valores = []
        for line in lines[6:]:
            valores.append([float(valor) for valor in line.split()])
        valores_matriz[fichero] = np.array(valores)

matrices_apiladas = np.stack(list(valores_matriz.values()))

desviacion_estandar_por_posicion = np.std(matrices_apiladas, axis=0)

first_lines = """ncols	1114
nrows	911
xllcorner	3629184.951183
yllcorner	2091206.641517
cellsize	30.000000
NODATA_value	-9999.000000
"""

for fitxer, matriu in valores_matriz.items():
    matriu_recalculada = matriu + 30 * desviacion_estandar_por_posicion
    matriu_recalculada = matriu_recalculada.round(4)
    new_file = fitxer.split('.')[0] + '_out.asc'
    with open(new_file, 'w') as cabesa:
        cabesa.write(first_lines)
        for row in matriu_recalculada:
            cabesa.write(' '.join(map(str, row)))
            cabesa.write('\n')