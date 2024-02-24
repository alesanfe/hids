import socket
import threading

import schedule
from loguru import logger

from src.main.python.repository import Repository


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
        self.repository.load_data()

    def start(self):
        """
        Start the server listening for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Aumentado el número de conexiones en cola

        logger.info(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()  # Accept incoming connection
            logger.info(f"Connection established from {addr}")

            # Manejar la comunicación con el cliente en un hilo separado
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """
        Handle an incoming client connection by sending a response to any messages it sends.

        Args:
            client_socket (socket): The socket for the incoming connection.
        """
        try:
            schedule.every().day.at("12:00").do(self.repository.all_files())

            while True:
                schedule.run_pending()
                data = client_socket.recv(1024)  # Recibir datos del cliente
                if not data:
                    break  # Si no hay datos, el cliente ha cerrado la conexión

                received_message = data.decode()
                logger.info(f"Received message from {client_socket.getpeername()}: {received_message}")

                self.repository.one_file(received_message)

                # Responder al cliente
                response_message = "Server received your message: " + received_message + " - " + str(self.km)
                client_socket.sendall(response_message.encode())
        except Exception as e:
            logger.info(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Aumentado el número de conexiones en cola

        logger.info(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()  # Accept incoming connection
            logger.info(f"Connection established from {addr}")

            # Manejar la comunicación con el cliente en un hilo separado
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)  # Recibir datos del cliente
                if not data:
                    break  # Si no hay datos, el cliente ha cerrado la conexión

                received_message = data.decode()
                logger.info(f"Received message from {client_socket.getpeername()}: {received_message}")



                # Responder al cliente
                response_message = self.repository.one_file(received_message)
                client_socket.sendall(str(response_message).encode('utf8'))
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    server = Server("localhost", 12345, "neo4j", "12345678")
    server.start()