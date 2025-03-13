import socket
import OpenSSL
from OpenSSL import SSL
import logging

# SSL certificate configuration
cert_file = "../ssl/fullchain.pem"
key_file = "../ssl/privkey.pem"

# Create SSL context for the server
context = SSL.Context(SSL.TLS_SERVER_METHOD)
context.use_certificate_file(cert_file)
context.use_privatekey_file(key_file)

# Server configuration
host = '0.0.0.0'
port = 8443

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Secure server listening on {host}:{port}")

# Accept incoming connections
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")


    # Wrap the socket in SSL
    ssl_socket = OpenSSL.SSL.Connection(context, client_socket)
    ssl_socket.set_accept_state()

    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print(f"📩 Received: {data.decode()}")
            ssl_socket.sendall(b"Message received securely!\n")
    except OpenSSL.SSL.Error as e:
        print(f"SSL Error: {e}")
    finally:
        ssl_socket.shutdown()
        ssl_socket.close()
