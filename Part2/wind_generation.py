import pandas as pd
import os
import subprocess
from datetime import datetime
from tqdm import tqdm
import shutil


path_wind = "PontVIladoma/Input/GIS_themes/PontViladomar_wind.wnd"

wind_df = pd.read_csv(path_wind, sep=' ', header=None, dtype={0: str, 1: str, 2: str})
wind_df.columns = ['mes', 'dia', 'hora', 'vel', 'dir', 'cloud']

windninja_cli_path = "C:/WindNinja/WindNinja-3.10.0/bin/WindNinja_cli"

config_file_path = "C:/Users/Usuario/Documents/stage2_SAP_final_proj/cli_domainAverage.cfg"

def write_config_file(vel, dir):
    with open(config_file_path, 'r') as f:
        config_data = f.readlines()
    
    for i, line in enumerate(config_data):
        if line.startswith("input_speed "):
            config_data[i] = f"input_speed = {vel}\n"
        elif line.startswith("input_direction"):
            config_data[i] = f"input_direction = {dir}\n"
    
    config_file_name = f"cli_domainAverage_{vel}_{dir}.cfg"
    with open(config_file_name, 'w') as f:
        f.writelines(config_data)
    
    return config_file_name

archivos_excluidos = ["Pont_de_Vilomar_2022_07_18_0020.lcp", "Pont_de_Vilomar_2022_07_18_0020.prj"]
directorio_origen = "C:/Users/Usuario/Documents/stage2_SAP_final_proj/PontVIladoma/Input/ASCII_files"

for index, row in tqdm(wind_df.iterrows(), total=len(wind_df), desc="Ejecutando WindNinja"):
    directorio_destino = f"WindNinja_results_{str(index)}"
    os.makedirs(directorio_destino)
    vel = row['vel']
    dir = row['dir']
    
    config_file_name = write_config_file(vel, dir)
    
    subprocess.run([windninja_cli_path, config_file_name], check=True)

    archivos = os.listdir(directorio_origen)
    for archivo in archivos:
        if archivo not in archivos_excluidos:
            ruta_origen = os.path.join(directorio_origen, archivo)
            ruta_destino = os.path.join(directorio_destino, archivo)
            shutil.move(ruta_origen, ruta_destino)
            print(f"Archivo {archivo} movido a {ruta_destino}")
            
    os.remove(config_file_name)