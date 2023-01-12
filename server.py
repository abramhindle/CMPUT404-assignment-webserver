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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        """
        Processes incoming requests from client
        """
        try:
            self.data = self.request.recv(1024).strip().decode()
            path = self.data.split(' ')[1]

            r = 'HTTP/1.1 404 NOT FOUND\n\nI do not know what you were trying to show, but it does not exist.'
            if path == '/':
                path = '/index.html'
                
            f = open('www' + path)
            contents = f.read()
            f.close() 

            if path.find('.css'):
                r = 'HTTP/1.1 200 OK\nContent-Type: text/css\n\n' + contents
            else: 
                r = 'HTTP/1.1 200 OK\n\n' + contents 
        except FileNotFoundError: 
            # currently is showing up even if the page shows...
            r = 'HTTP/1.1 404 NOT FOUND\n\nI do not know what you were trying to show, but it does not exist.'
        finally: 
            self.request.sendall(r.encode('utf-8')) # send the HTML page with CSS styling
            self.request.close() # close the client connection

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    print('Webserver running on port %s' % PORT)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
