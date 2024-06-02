import os
import shutil


def extraer_linea_3_y_concatenar(directorio, archivo_salida):
    path = "/home/wrf-chem/Desktop/FARSITE4/PontVIladoma/Input/custom_wind/"
    with open(archivo_salida, 'w') as archivo_final:
        for carpeta_raiz, subcarpetas, archivos in os.walk(directorio):
            try:
                if carpeta_raiz.split('\\')[1] == "wind_simulations":
                    i = carpeta_raiz.split('\\')[2].split('_')[2]
            except:
                pass
            for nombre_archivo in archivos:
                if nombre_archivo.endswith('.atm'):
                    ruta_archivo = os.path.join(carpeta_raiz, nombre_archivo)
                    try:
                        with open(ruta_archivo, 'r') as archivo:
                            lineas = archivo.readlines()
                            if len(lineas) >= 3:
                                arxius = lineas[2].split(' ')
                                archivo_final.write(arxius[0]+ " " + arxius[1]+ " " + arxius[2]+ " " + path + 
                                                    arxius[3].split('.')[0]+'_out' + '_' + str(i) + '.' + arxius[3].split('.')[1] + ' ' 
                                                    + path + arxius[4].split('.')[0] + '_' + str(i) + '.' +  arxius[4].split('.')[1] + ' '
                                                    + path + arxius[5].split('.')[0] + '_' + str(i) + '.' +  arxius[5].split('.')[1])
                    except Exception as e:
                        print(f"Error al leer el archivo {ruta_archivo}: {e}")

def guardar_atm(directory):
    destino = os.path.join(directory, 'custom_wind')
    
    # Crea la carpeta destino si no existe
    if not os.path.exists(destino):
        os.makedirs(destino)

    i = 0
    for carpeta_raiz, subcarpetas, archivos in os.walk(directory):
        try:
            if carpeta_raiz.split('\\')[1] == "wind_simulations":
                i = carpeta_raiz.split('\\')[2].split('_')[2]
        except:
            pass
        for nombre_archivo in archivos:
            if nombre_archivo.endswith('.asc') and not nombre_archivo.endswith('vel.asc'):
                nombre_archivo_aux = nombre_archivo.split('.')[0] + '_' + str(i) + '.' + nombre_archivo.split('.')[1]
                os.rename(os.path.join(carpeta_raiz, nombre_archivo), os.path.join(carpeta_raiz, nombre_archivo_aux))
                # Define las rutas completa del archivo origen y destino
                ruta_archivo = os.path.join(carpeta_raiz, nombre_archivo_aux)
                # Mueve el archivo a la carpeta destino
                shutil.copy(ruta_archivo, destino)
                print(f'Movido: {nombre_archivo_aux} a {destino}')
        


directorio = '.'
archivo_salida = 'final.atm'

extraer_linea_3_y_concatenar(directorio, archivo_salida)
guardar_atm(directorio)

