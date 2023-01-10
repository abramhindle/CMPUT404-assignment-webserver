import socket 

HOST, PORT = "localhost", 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((HOST, PORT))

    s.sendall('Are you there?'.encode('UTF-8'))
    received = str(s.recv(1024).decode())

    print("Sent:     {}".format('Are you there?'))
    print("Received: {}".format(received))
except: 
    print("Connection failed.")
