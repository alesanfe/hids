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
        mes_anterior = mes_actual -1
        año_anterior = año_actual

    patrón=os.path.join(path, f"{año_anterior:04d}-{mes_anterior:02d}-*.txt")
    logs_del_mes = glob.glob(patrón)

    return logs_del_mes

def obtener_archivos_no_integros(ultimo_log):

    archivos_no_integros = []

    try:
        with open(ultimo_log, 'r', encoding='utf-8') as archivo:
            print(ultimo_log)
            for linea in archivo:
                archivo = re.search(r"File ([^\s]+) has been modified", linea)
                if archivo:
                    nombre_archivo = archivo.group(1)
                    archivos_no_integros.append(os.path.basename(nombre_archivo))

    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
    return archivos_no_integros

def obtener_archivos_no_integros_por_dia(lista_log):
    archivos_no_integros = set()
    for log in lista_log:
        try:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', log)
            fecha = match.group(1)
            with open(log, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    archivo = re.search(r"File ([^\s]+) has been modified", linea)
                    if archivo:
                        nombre_archivo = archivo.group(1)
                        archivos_no_integros.add((nombre_archivo,fecha))
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")
    return archivos_no_integros

def compilar_informe_mensual_por_dia():
    lista_logs = procesar_logs_diarios()
    archivos_no_integros=obtener_archivos_no_integros_por_dia(lista_logs)
    archivos_no_integros_actualmente=obtener_archivos_no_integros(lista_logs[-1])
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year
    archivos_ordenados = sorted(list(archivos_no_integros), key=lambda x: x[0])

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
        archivo_informe.write("=" * 50 + "\n")
        archivo_informe.write(f"Informe Mensual - {mes_anterior:02d}/{año_anterior:04d}\n")
        archivo_informe.write("=" * 50 + "\n\n")

        archivo_informe.write("Archivos No Íntegros Actualmente:\n")
        for archivo in archivos_no_integros_actualmente:
            archivo_informe.write(f"\t- {archivo};\n")
        archivo_informe.write("\n")

        archivo_informe.write("Archivos No Íntegros Durante el Mes:\n")
        for elemento in archivos_ordenados:
            partes_fecha = elemento[1].split("-")
            fecha_invertida = "-".join(reversed(partes_fecha))
            archivo_informe.write(f"\t- Archivo en ruta {elemento[0]} dejó de ser íntegro el {fecha_invertida};\n")
        archivo_informe.write("\n")
        archivo_informe.write("=" * 50 + "\n")

        archivo_informe.write("Último Log Diario:\n")
        archivo_informe.write("\t"+lista_logs[-1].replace("../logs\\", "")+"\n")
        archivo_informe.write("=" * 50 + "\n\n")

    print(f"Informe mensual compilado en: {ruta_archivo_informe}")
# Ejemplo de us
if __name__ == "__main__":
    #compilar_informe_mensual()
    compilar_informe_mensual_por_dia()
