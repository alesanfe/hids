import socket
import OpenSSL
from OpenSSL import SSL

# Path to the certificate file (used for verification)
cert_file = "../ssl/fullchain.pem"

# Create SSL context for the client
context = SSL.Context(SSL.TLS_CLIENT_METHOD)
# context.load_verify_locations(cert_file)

# Create the client socket
client_socket = socket.create_connection(("127.0.0.1", 8443))

# Wrap the socket in SSL
ssl_socket = OpenSSL.SSL.Connection(context, client_socket)
ssl_socket.set_connect_state()
ssl_socket.do_handshake()

try:
    print("Secure connection established with the server.")

    while True:
        msg = input("Send message: ")
        ssl_socket.sendall(msg.encode())

        response = ssl_socket.recv(1024)
        print(f"Server response: {response.decode()}")
finally:
    ssl_socket.shutdown()
    ssl_socket.close()
