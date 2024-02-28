import os
import socket
import threading
import time
from queue import Queue

import schedule
import concurrent.futures

from src.main.python.logger import Logger
from src.main.python.repository import Repository

logger = Logger()

class Server:
    """
    This class implements a simple TCP server that listens for incoming connections
    and sends back a response to any message it receives. The server also tracks the
    number of messages it has received and returns that count in its response.
    """

    def __init__(self, host, port, user, password):
        """
        Initialize the server with the specified host and port.

        Args:
            host (str): The hostname or IP address to bind to.
            port (int): The port number to listen on.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.repository = Repository(user, password)
        self.repository.delete_all()
        self.repository.load_data()

    def start(self):
        """
        Start the server listening for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Increased the number of connections in the queue

        logger.info(f"Server listening on {self.host}:{self.port}")

        queue_for_scheduler = Queue()
        threading.Thread(target=self.print_hello, args=(queue_for_scheduler,)).start()

        print("Hello")

        # Ejecuta self.repository.all_files() en segundo plano cada 10 segundos
        schedule.every(10).seconds.do(lambda: self.execute_non_blocking(self.repository.all_files))

        while True:
            client_socket, addr = self.server_socket.accept()  # Accept incoming connection
            logger.info(f"Connection established from {addr}")

            # Handle communication with the client in a separate thread
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            print("hello")

        print("adiós")

    def print_hello(self, queue_for_scheduler):
        """
        Print "hola" every second.
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute_non_blocking(self, func):
        """
        Execute a function in a separate thread.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(func)

    def handle_client(self, client_socket):
        """
        Handle an incoming client connection by sending a response to any messages it sends.

        Args:
            client_socket (socket): The socket for the incoming connection.
        """
        try:
            while True:
                try:
                    data = client_socket.recv(1024)  # Recibe datos del cliente
                    if not data:
                        break  # Si no hay datos, el cliente ha cerrado la conexión

                    received_message = data.decode()
                    logger.info(f"Received message from {client_socket.getpeername()}: {received_message}")

                    message = self.actions(received_message)

                    chunk_size = 1024
                    for i in range(0, len(message), chunk_size):
                        chunk = message[i:i + chunk_size]
                        print(chunk)
                        client_socket.sendall(chunk.encode("utf-8"))

                    # Send the end indicator
                    client_socket.sendall("END".encode("utf-8"))

                except socket.timeout:
                    pass  # Se alcanzó el tiempo de espera, continua con el siguiente ciclo

        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def actions(self, received_message):
        print(received_message.startswith("log"))
        if received_message.startswith("all_files"):
            message = "|".join([file for _, _, aux_files in os.walk("../resources") for file in aux_files if "." in file])
        elif received_message.startswith("all_logs"):
            message = "|".join(os.listdir("../logs"))
        elif received_message.startswith("file"):
            file = received_message[5:]
            message = str(self.repository.one_file(file))
        elif received_message.startswith("log"):
            file = received_message[4:]
            path_element = os.path.join("../logs", file)
            with open(path_element, 'r', encoding='utf-8') as file:
                message = file.read()
        return message
