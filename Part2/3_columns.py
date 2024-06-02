# Leer el primer fichero
with open('C:/Users/Usuario/Documents/stage2_SAP_final_proj/wind_simulations/PontViladomar_wind.wnd', 'r') as file:
    primer_fichero_lineas = file.readlines()

# Leer el segundo fichero
with open('C:/Users/Usuario/Documents/stage2_SAP_final_proj/wind_simulations/final.atm', 'r') as file:
    segundo_fichero_lineas = file.readlines()

# Abrir el fichero para escribir el resultado
with open('fichero_resultante.txt', 'w') as file:
    for i, linea_primer_fichero in enumerate(primer_fichero_lineas):
        # Separar la línea en columnas
        columnas_primer_fichero = linea_primer_fichero.strip().split(' ')
        columnas_segundo_fichero = segundo_fichero_lineas[i].strip().split(' ')

        # Reemplazar las tres primeras columnas
        columnas_segundo_fichero[:3] = columnas_primer_fichero[:3]

        # Escribir la línea resultante en el fichero
        file.write(' '.join(columnas_segundo_fichero) + '\n')

print("El fichero ha sido procesado y guardado como 'fichero_resultante.txt'")
