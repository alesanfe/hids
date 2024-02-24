
import logging
import os
from datetime import datetime

from loguru import logger
from neomodel import config

from integrity_vertification import check_integrity

def configurar_logger():
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    # Crear un nombre de archivo con la fecha
    nombre_archivo_log = f'{fecha_actual}_error_log.txt'
    ruta_archivo_log = os.path.join('../logs', nombre_archivo_log)
    os.makedirs('logs', exist_ok=True)

    # Configurar el logger de Loguru
    logger.add(ruta_archivo_log, level="ERROR", rotation="1 day", retention="7 days", compression="zip")


if __name__ == "__main__":
    config.DATABASE_URL = 'bolt://neo4j:ssii1234@localhost:7687'
    configurar_logger()
    check_integrity()
