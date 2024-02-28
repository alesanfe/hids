import os
import glob
import re
from datetime import datetime

def procesar_logs_diarios():
    path="../logs"
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    # Calcular el mes y año del mes anterior
    if mes_actual == 1:
        mes_anterior = 12
        año_anterior = año_actual - 1
    else:
        mes_anterior = mes_actual
        año_anterior = año_actual

    patrón=os.path.join(path, f"{año_anterior:04d}-{mes_anterior:02d}-*.txt")
    logs_del_mes = glob.glob(patrón)

    return logs_del_mes

def obtener_archivos_no_integros(ultimo_log):

    archivos_no_integros = []

    try:
        with open(ultimo_log, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                archivo = re.search(r"File ([^\s]+) has been modified", linea)
                if archivo:
                    nombre_archivo = archivo.group(1)
                    archivos_no_integros.append(nombre_archivo)

    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
    print(archivos_no_integros)
    return archivos_no_integros

def compilar_informe_mensual():
    lista_logs = procesar_logs_diarios()
    archivos_no_integros=obtener_archivos_no_integros(lista_logs[-1])
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    # Crear la carpeta de destino si no existe
    if not os.path.exists("../monthly_reports"):
        os.makedirs("../monthly_reports")

    if mes_actual == 1:
        mes_anterior = 12
        año_anterior = año_actual - 1
    else:
        mes_anterior = mes_actual - 1
        año_anterior = año_actual

    # Crear el nombre del archivo del informe mensual
    nombre_informe = f"Informe-{año_anterior:04d}_{mes_anterior:02d}.txt"
    ruta_archivo_informe = os.path.join("../monthly_reports/", nombre_informe)

    # Escribir el informe mensual
    with open(ruta_archivo_informe, 'w', encoding='utf-8') as archivo_informe:
        archivo_informe.write(f"Intervalo de tiempo del informe mensual: {año_anterior:04d}_{mes_anterior:02d}\n\n")
        archivo_informe.write("Lista de archivos no íntegros:\n")
        archivo_informe.write("\n".join(archivos_no_integros))
        archivo_informe.write("\n\n")
        archivo_informe.write("Último log diario:\n")
        archivo_informe.write(lista_logs[-1])

    print(f"Informe mensual compilado en: {ruta_archivo_informe}")

# Ejemplo de us
if __name__ == "__main__":
    compilar_informe_mensual()
