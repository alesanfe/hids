import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connection established with server at {self.host}:{self.port}")

    def send_message(self, message):
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
            print(f"Sent message to server: {message}")
            # Add any additional logic here, such as waiting for a response from the server
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_message(self):
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
                data = self.client_socket.recv(1024).decode()  # Receive data from the client
                if data == "END":
                    break  # If no data, the client has closed the connection
                message += data

            print(f"Received message from server: {message}")
            return message
        except Exception as e:
            print(f"Error receiving message: {e}")

    def close(self):
        """
        Closes the connection with the server.
        """
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")

