#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Kezziah Camille Ayuno
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
        Only processes GET requests
        """
        try:
            self.data = self.request.recv(1024).strip().decode()
            print('Got a request: \n' + self.data)
            if self.data != ' ' or self.data != '':
                s_data = self.data.split(' ')
                method, path = s_data[0], s_data[1]
            
            if method != 'GET':
                header = 'HTTP/1.1 405 Method Not Allowed\n'
            else: 
                header = 'HTTP/1.1 200 OK\n'

            root = 'www'
            r = ''

            if path == '/':
                path = '/index.html'
            
            if not path.endswith('/') and not path.endswith('.css') and not path.endswith('.html'):
                header = 'HTTP/1.1 301 Moved Permanently'
                r = header + '\nLocation: ' + path + '/'
            else:            
                f = open(root + path)
                contents = f.read()
                f.close() 

                if path.endswith('.css'):
                    r = header + 'Content-Type: text/css\n\n' + contents
                elif path.endswith('.html'):
                    r = header + 'Content-Type: text/html\n\n' + contents
        except IsADirectoryError:
            if os.path.isfile(root + path + 'index.html'):
                f = open(root + path + 'index.html')
                contents = f.read()
                f.close()
                r = header + 'Content-Type: text/html\n\n' + contents
            else:
                r = 'HTTP/1.1 404 NOT FOUND\n\nI do not know what you were trying to show, but it does not exist.'
        except FileNotFoundError: 
            r = 'HTTP/1.1 404 NOT FOUND\n\nI do not know what you were trying to show, but it does not exist.'
        finally: 
            self.request.sendall(r.encode('utf-8'))
            self.request.close()

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    with socketserver.TCPServer((HOST, PORT), MyWebServer) as server:
        print('Running on port %s' % PORT)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
