import socket

from OpenSSL import SSL


class Client:
    """
    Client for communication with an SSL-enabled server.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the client.
        """
        self.host = host
        self.port = port
        self.client_socket = None
        self.context = self._create_ssl_context()

    def _create_ssl_context(self) -> SSL.Context:
        """
        Create and configure an SSL context using PyOpenSSL.
        """
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        context.load_verify_locations("../ssl/fullchain.pem")
        return context

    def connect(self) -> None:
        """
        Establishes a connection to the server using SSL.
        """
        # raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # raw_socket.connect((self.host, self.port))
        raw_socket = socket.create_connection((self.host, self.port))

        self.client_socket = SSL.Connection(self.context, raw_socket)
        self.client_socket.set_connect_state()
        self.client_socket.do_handshake()

    def send_message(self, message: str) -> None:
        """
        Send a message to the server.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        self.client_socket.sendall(message.encode())

    def receive_message(self) -> str:
        """
        Receive a message from the server.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        message = ""
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if not data or data.endswith("END"):
                    break
                if data:
                    message += data
        except SSL.Error as e:
            print(f"SSL Error: {e}")
        return message.strip("END")


def close(self) -> None:
    """
    Close the connection.
    """
    if self.client_socket:
        self.client_socket.shutdown()
        self.client_socket.close()
        self.client_socket = None
