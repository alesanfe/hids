import os
import socket
import threading
import schedule

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

        while True:
            client_socket, addr = self.server_socket.accept()  # Accept incoming connection
            logger.info(f"Connection established from {addr}")

            # Handle communication with the client in a separate thread
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """
        Handle an incoming client connection by sending a response to any messages it sends.

        Args:
            client_socket (socket): The socket for the incoming connection.
        """
        try:
            schedule.every().day.at("12:00").do(self.repository.all_files)

            while True:
                schedule.run_pending()
                data = client_socket.recv(1024)  # Receive data from the client


                if not data:
                    break  # If no data, the client has closed the connection

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