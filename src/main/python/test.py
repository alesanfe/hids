import os
import random
from configparser import ConfigParser

from colorama import Fore, Style

from repository import Repository
from logger import Logger


class Test:
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    # DB
    user = config.get("DB", "user")
    password = config.get("DB", "password")
    def __init__(self, cantidad_carpetas, cantidad_archivos):
        self.cantidad_carpetas = cantidad_carpetas
        self.cantidad_archivos = cantidad_archivos

    def generar_archivos_y_carpetas(self):
        # Crear la carpeta "resources" si no existe
        if not os.path.exists("../resources/"):
            os.makedirs("../resources/")

        # Generar carpetas
        for i in range(1, self.cantidad_carpetas + 1):
            carpeta_nombre = f"test_folder_{i}"
            carpeta_path = os.path.join("../resources/", carpeta_nombre)
            if not os.path.exists(carpeta_path):
                os.makedirs(carpeta_path)

            # Generar archivos
            for j in range(1, self.cantidad_archivos + 1):
                archivo_nombre = f"file_{i}_{j}.txt"
                archivo_path = os.path.join(f"../resources/test_folder_{i}/", archivo_nombre)
                with open(archivo_path, "w") as archivo:
                    # Escribir algo en el archivo (puedes personalizar esto)
                    archivo.write(f"Contenido del archivo {j}")

    def borrar_archivos_y_carpetas(self):
        # Borrar carpetas generadas por generar_archivos_y_carpetas() que empiecen por "test"
        if os.path.exists("../resources/"):
            for root, dirs, files in os.walk("../resources/", topdown=False):
                for dir in dirs:
                    if dir.startswith("test_folder_"):
                        dir_path = os.path.join(root, dir)
                        dir_full_path = os.path.join(root, dir)
                        for file in os.listdir(dir_full_path):
                            file_path = os.path.join(dir_full_path, file)
                            os.remove(file_path)
                        os.rmdir(dir_path)
        with open("../logs/9999-99-99_error_log.txt", 'w') as archivo:
            archivo.truncate()
        print("Carpetas generadas por el test borradas.")

    def modificar_archivo(self, carpeta, archivo):
        # Modificar un archivo dentro de una carpeta específica
        archivo_path = os.path.join(f"../resources/test_folder_{carpeta}", f"file_{carpeta}_{archivo}.txt")

        if os.path.exists(archivo_path):
            with open(archivo_path, "a", encoding='utf-8') as archivo:
                # Modificar el contenido del archivo
                archivo.write("\nModificación en el archivo.")
            print(f"Se ha modificado: {archivo_path}")

    def mirar_logs(self):
        try:
            with open("../logs/9999-99-99_error_log.txt", 'r') as file:
                lineas = file.readlines()
                cantidad_lineas = len(lineas)
                return cantidad_lineas
        except FileNotFoundError:
            print(f"El archivo no fue encontrado.")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def test1_modificacion_un_archivo_con_one_file(self):
        self.generar_archivos_y_carpetas()
        logger = Logger(is_test=True)
        repository = Repository(self.user, self.password)
        repository.load_data()
        archivo = random.randint(1, cantidad_archivos)
        carpeta=random.randint(1, cantidad_carpetas)
        self.modificar_archivo(carpeta, archivo)
        repository.one_file(f"file_{carpeta}_{archivo}.txt")

        print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Archivo modificado:{Style.RESET_ALL} file_{carpeta}_{archivo}.txt")
        print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}\n")

        result = self.mirar_logs()

        if result == 1:
            print(f"{Fore.GREEN}Solo se ha modificado un archivo.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}El test ha fallado.{Style.RESET_ALL}")

        self.borrar_archivos_y_carpetas()

    def test2_modificar_todo_con_all_files(self):
        self.generar_archivos_y_carpetas()
        logger = Logger(is_test=True)
        repository = Repository(self.user, self.password)
        repository.load_data()
        for i in range(1, self.cantidad_carpetas + 1):
            for j in range(1, self.cantidad_archivos + 1):
                self.modificar_archivo(i, j)
        repository.all_files()
        result = self.mirar_logs()

        if result == cantidad_archivos*cantidad_carpetas:
            print(f"{Fore.GREEN}Se han modificado {result} archivos, el test es correcto.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}El test ha fallado.{Style.RESET_ALL}")

        self.borrar_archivos_y_carpetas()

    def test3_modificar_un_archivo_con_all_files(self):
        self.generar_archivos_y_carpetas()
        logger = Logger(is_test=True)
        repository = Repository(self.user, self.password)
        repository.load_data()
        archivo = random.randint(1, cantidad_archivos)
        carpeta = random.randint(1, cantidad_carpetas)
        self.modificar_archivo(carpeta, archivo)
        repository.all_files()

        print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Archivo modificado:{Style.RESET_ALL} file_{carpeta}_{archivo}.txt")
        print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}\n")

        result = self.mirar_logs()

        if result == 1:
            print(f"{Fore.GREEN}Solo se ha modificado un archivo.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}El test ha fallado.{Style.RESET_ALL}")

        self.borrar_archivos_y_carpetas()

    def test4_modificar_cero_archivos_con_one_file(self):
        self.generar_archivos_y_carpetas()
        logger = Logger(is_test=True)
        repository = Repository(self.user, self.password)
        repository.load_data()
        archivo = random.randint(1, cantidad_archivos)
        carpeta = random.randint(1, cantidad_carpetas)
        repository.one_file(f"../resources/test_folder_{carpeta}", f"file_{carpeta}_{archivo}.txt")
        result = self.mirar_logs()

        if result == 0:
            print(f"{Fore.GREEN}No se ha modificado ningún archivo.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}El test ha fallado.{Style.RESET_ALL}")

        self.borrar_archivos_y_carpetas()

    def test5_modificar_cero_archivos_con_all_files(self):
        self.generar_archivos_y_carpetas()
        logger = Logger(is_test=True)
        repository = Repository(self.user, self.password)
        repository.load_data()
        repository.all_files()
        result = self.mirar_logs()

        if result == 0:
            print(f"{Fore.GREEN}No se ha modificado ningún archivo.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}El test ha fallado.{Style.RESET_ALL}")

        self.borrar_archivos_y_carpetas()

if __name__=="__main__":
    cantidad_carpetas = 3
    cantidad_archivos = 5

    test_instance = Test(cantidad_carpetas, cantidad_archivos)
    test_instance.test1_modificacion_un_archivo()
    test_instance.test2_modificar_todo_con_all_files()
    test_instance.test3_modificar_un_archivo_con_all_files()
    test_instance.test4_modificar_cero_archivos_con_one_file()
    test_instance.test5_modificar_cero_archivos_con_all_files()
