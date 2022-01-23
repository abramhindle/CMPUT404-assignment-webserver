import socket
import sys

HOST, PORT = "localhost", 8080

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))


    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Starting client connection...")
print("Received: {}".format(received))
