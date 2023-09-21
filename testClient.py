import socket

BYTES_TO_READ = 4096
FORMAT = 'utf-8'
PORT = 8080
HOST = "localhost"

def get(host, port, path):
    request = b"GET " + path.encode(FORMAT) + b" HTTP/1.1\r\nHost: " + host.encode(FORMAT) + b"\r\n\r\n"
    #could also use f string --> f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode(FORMAT)
    # Creates a client socket using IPv4 and TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(request)
    client.shutdown(socket.SHUT_WR)
    result = client.recv(BYTES_TO_READ)
    while (len(result)) > 0:
        print(result.decode(FORMAT))
        result = client.recv(BYTES_TO_READ)

    client.close()

path = "/base.css"

get(HOST, PORT, path)