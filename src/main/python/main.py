import threading
from configparser import ConfigParser

from interface import InterfaceHIDS
from server import Server

if __name__ == '__main__':
    config = ConfigParser()
    config.read("config.ini")

    # SERVER
    host = config.get("SERVER", "host")
    port = config.get("SERVER", "port")

    # DB
    user = config.get("DB", "user")
    password = config.get("DB", "password")

    server = Server(host, int(port), user, password)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    interface = InterfaceHIDS(host, int(port))

    server_thread.join()


