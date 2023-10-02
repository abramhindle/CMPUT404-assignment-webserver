#  coding: utf-8 
import socketserver, os

# Copyright 2023 Shalomi Hron
#
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #self.data = None # TODO: test unreadable request
        if self.data == None:
            # Badly formatted request
            self.request.sendall(bytearray("HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n"+"<body><h1>400: Bad Request</h1></body>\r\n",'utf-8'))

        self.plainData = self.data.decode().split()
        method, path, protocol = self.plainData[0:3]

        # Confirm method can be handled
        if self.plainData[0] == "GET":
            self.handleGet(path)
        else:
            # Return 405 error for any method that you cannot handle
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n"+"<body><h1>405: Method Not Allowed</h1></body>\r\n",'utf-8'))


    def handleGet(self, path):
        pathEnd = path.split("/")[-1] # Is the deepest path of the path a file?
        
        # Check if we need a 301 code to correct the path ending where no file is requested.
        if (path[-1] != "/") and (not "." in pathEnd):
            path += "/"
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: "+path+"\r\n",'utf-8'))
        else:
            # For correct path endings, confirm the rest of the path is correct.
            path = "/www" + path # the webserver serves files from ./www
            refDirectory = os.path.dirname(os.path.realpath(__file__))
            fullLocation = refDirectory + path

            # If the path is correct, then serve the specified file, or the index.html file if none is specified
            if os.path.exists(fullLocation):
                self.serveFiles(path, fullLocation)
            else:
                # The directory itself does not exist
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"+"<body><h1>404: Not Found</h1></body>\r\n",'utf-8'))


    def serveFiles(self, path, fullLocation):
        if "." in path:
            # Try serving the file
            try:
                with open(fullLocation, 'r') as file:
                    file_content = file.read() 

                # Send the proper file mime-types
                fileType = path.split(".")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/" + fileType[1]+"\r\n\r\n"+file_content+"\r\n",'utf-8'))
            except FileNotFoundError:
                print("Error: the path is invalid / the file does not exist.")
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"+"<body><h1>404: Not Found</h1></body>\r\n",'utf-8'))
            except:
                print("Error: Unable to load the file.")
                # 500 Internal Server Error
                self.request.sendall(bytearray("HTTP/1.1 500 Internal Server Error\r\n",'utf-8'))
        else:
            # If no file was specified, try serving index.html
            try:
                with open(fullLocation + "index.html", 'r') as file:
                    file_content = file.read() 
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+file_content+"\r\n",'utf-8'))
            except FileNotFoundError:
                print("Error: the path is invalid / the file does not exist.")
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"+"<body><h1>404: Not Found</h1></body>+\r\n",'utf-8'))
            except:
                print("Error: Unable to load the file.")
                # 500 Internal Server Error
                self.request.sendall(bytearray("HTTP/1.1 500 Internal Server Error\r\n",'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
