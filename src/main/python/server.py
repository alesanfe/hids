import concurrent.futures
import os
import socket
import threading
import time
from typing import Callable, List
import OpenSSL
from OpenSSL import SSL
import schedule
import select

from logger import load_logger
from monthly_report import compile_monthly_report_by_day
from repository import Repository


class Server:
    """
    This class implements a simple TCP server that listens for incoming connections
    with SSL enabled using PyOpenSSL.
    """

    def __init__(self, port: int, user: str, password: str, host_db: str,
                 resources: List[str] = None) -> None:
        """
        Initialize the server with the specified host, port, and SSL settings.
        """
        self.port = port
        self.server_socket = None
        self.repository = Repository(user, password, host_db, resources)
        self.context = self._create_ssl_context()

        self.repository.delete_all()
        self.repository.load_data()
        self.resources = resources if resources is not None else []

    def _create_ssl_context(self) -> SSL.Context:
        """
        Creates and configures an SSL context using PyOpenSSL.
        """
        cert_file = "../ssl/fullchain.pem"
        key_file = "../ssl/privkey.pem"

        context = SSL.Context(SSL.TLS_SERVER_METHOD)
        context.use_certificate_file(cert_file)
        context.use_privatekey_file(key_file)
        return context

    def start(self) -> None:
        """
        Start the server with SSL enabled, listening for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(5)

        print(f"Server listening on 0.0.0.0:{self.port}")

        load_logger()
        threading.Thread(target=self.print_scheduler, daemon=True).start()

        schedule.every(1).days.do(lambda: self.execute_non_blocking(self.repository.all_files))
        schedule.every(30).days.do(lambda: self.execute_non_blocking(compile_monthly_report_by_day))

        while True:
            client_socket, _ = self.server_socket.accept()
            ssl_client_socket = SSL.Connection(self.context, client_socket)
            ssl_client_socket.set_accept_state()
            threading.Thread(target=self.handle_client, args=(ssl_client_socket,), daemon=True).start()

    def print_scheduler(self) -> None:
        """
        Run scheduled tasks.
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute_non_blocking(self, func: Callable) -> None:
        """
        Execute a function in a separate thread.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(func)

    def handle_client(self, client_socket) -> None:
        """
        Handle an incoming client connection.
        """
        try:
            while True:
                active, _, _ = select.select([client_socket], [], [], 1)
                if not active:
                    continue

                data = client_socket.recv(1024)
                if not data:
                    break

                received_message = data.decode()
                message = self.actions(received_message)

                chunk_size = 512
                for i in range(0, len(message), chunk_size):
                    chunk = message[i:i + chunk_size]
                    client_socket.sendall(chunk.encode("utf-8"))

                client_socket.sendall("END".encode("utf-8"))
        except OpenSSL.SSL.Error as e:
            print(f"SSL Error: {e}")
        finally:
            client_socket.shutdown()
            client_socket.close()

    def actions(self, received_message: str) -> str:
        """
        Process incoming messages.
        """
        if received_message.startswith("all_files"):
            message = "|".join(
                [file for resource in self.resources for _, _, aux_files in os.walk(resource) for file in aux_files if
                 "." in file])
        elif received_message.startswith("all_logs"):
            message = "|".join(os.listdir("../logs"))
        elif received_message.startswith("all_reports"):
            message = "|".join(os.listdir("../reports"))
        elif received_message.startswith("file"):
            file = received_message[5:]
            message = str(self.repository.one_file(file))
        elif received_message.startswith("log"):
            file = received_message[4:]
            path_element = os.path.join("../logs", file)
            with open(path_element, 'r', encoding='utf-8') as file:
                message = file.read()
        elif received_message.startswith("report"):
            file = received_message[7:]
            path_element = os.path.join("../reports", file)
            with open(path_element, 'r', encoding='utf-8') as file:
                message = file.read()
        return message
