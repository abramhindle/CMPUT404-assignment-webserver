#  coding: utf-8 
import socketserver

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

FORMAT = 'utf-8'


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        print(f"DATA --> {self.data}\n\n\n")
        requestInput = self.data.decode(FORMAT).split('\n')
        print(f"REQUEST INPUT --> {requestInput}\n\n\n")
        requestLine = requestInput[0].split()
        print(f"REQUEST LINE --> {requestLine}\n\n\n")
        method = requestLine[0]
        path = requestLine[1]
        print(f"METHOD --> {method}\n\n\n")
        print(f"PATH --> {path}\n\n\n")


        if method == "GET":
            #maybe make more general get request method in the future?
            if path == "/base.css":
                self.serveCSS()
            else:
                print("PATH != /base.css")
                
        else:
            print("METHOD != GET")
            


        #parse_lines = self.data.decode
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n\r\nOK", FORMAT))

    def serveCSS(self):
        print("Serve css function")

        responseHeader = "HTTP/1.1 200 OK\r\n"

        content = ""
        try:
            with open("./www/base.css", "r") as cssFile:
                content = cssFile.read()
        except FileNotFoundError:
            responseHeader = "HTTP/1.1 404 Not Found\r\n"
            content = "EMPTY"

        self.request.sendall(responseHeader.encode(FORMAT) + content.encode(FORMAT))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    print("--- Server Running ---")

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
