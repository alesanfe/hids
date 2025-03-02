import socket
import ssl

class Client:
    """
    The Client class facilitates communication with a server using a socket connection
    over SSL.
    """

    def __init__(self, host: str, port: int, ssl_enabled: bool = True) -> None:
        """
        Initializes a Client instance with the specified host, port, and SSL option.

        Args:
            host (str): Hostname or IP address of the server.
            port (int): Port number for the connection.
            ssl_enabled (bool): Whether to use SSL for the connection (default is True).
        """
        self.host = host
        self.port = port
        self.ssl_enabled = ssl_enabled
        self.client_socket = None

    def connect(self) -> None:
        """
        Establishes a connection to the server, optionally using SSL.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        if self.ssl_enabled:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            # You can use context.load_cert_chain() to provide the client's certificate if needed
            self.client_socket = context.wrap_socket(self.client_socket, server_hostname=self.host)

    def send_message(self, message: str) -> None:
        """
        Sends a message to the connected server.

        Args:
            message (str): The message to be sent.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        try:
            self.client_socket.sendall(message.encode())
        except Exception:
            pass

    def receive_message(self) -> str:
        """
        Receives a message from the connected server.

        Returns:
            str: The message received.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        try:
            message = ""
            while True:
                data = self.client_socket.recv(1024).decode()
                if data == "END":
                    break
                message += data

            return message
        except Exception:
            pass

    def close(self) -> None:
        """
        Closes the connection with the server.
        """
        if self.client_socket:
            self.client_socket.close()


