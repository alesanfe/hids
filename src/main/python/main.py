import threading
import os
from server import Server
from src.main.python.interface import InterfaceHIDS

if __name__ == '__main__':
    # Obtener las variables de entorno
    host = os.getenv('SERVER_HOST', 'localhost')  # Valor por defecto si no se encuentra la variable
    port = int(os.getenv('SERVER_PORT', 8080))  # Valor por defecto si no se encuentra la variable

    # Configuración de la base de datos
    db_host = os.getenv('DB_HOST', 'localhost')  # Valor por defecto si no se encuentra la variable
    db_user = os.getenv('DB_USER', 'neo4j')  # Valor por defecto si no se encuentra la variable
    db_password = os.getenv('DB_PASSWORD', '12345678')  # Valor por defecto si no se encuentra la variable

    # Obtener las rutas de recursos desde la variable de entorno RESOURCES_PATHS
    resources_paths = os.getenv('RESOURCES_PATHS', '')  # Valor por defecto es una cadena vacía si no existe
    resources = resources_paths.split(';') if resources_paths else [
        r"C:\Users\alex0\Documents\ZAP"]  # Si no existe, usar el valor por defecto

    # Crear el servidor con la lista de recursos
    server = Server(port, db_user, db_password, db_host, resources)

    # Iniciar el servidor en un hilo
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Si necesitas la interfaz, descomenta la siguiente línea y ajusta según sea necesario:
    interface = InterfaceHIDS(host, port)

    # Esperar a que el hilo del servidor termine
    server_thread.join()
