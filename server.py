#  coding: utf-8 
import socketserver
import os

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
'''
        Example structure(s) of decoded:

        DECODED
        GET /hardcode/index.html HTTP/1.1
        Accept-Encoding: identity
        Host: 127.0.0.1:8080
        User-Agent: Python-urllib/3.8
        Connection: close

        DECODED
        PUT /base.css HTTP/1.1
        Accept-Encoding: identity
        Content-Type: application/x-www-form-urlencoded
        ontent-Length: 8
        Host: 127.0.0.1:8080
        User-Agent: Python-urllib/3.8
        Connection: close
'''
'''
        SECTIONS [b'GET', b'/base.css', b'HTTP/1.1', b'Accept-Encoding:', b'identity', b'Host:', 
        b'127.0.0.1:8080', b'User-Agent:', b'Python-urllib/3.8', b'Connection:', b'close']
'''
BASE_PATH = 'www'

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #print("Path", BASE_PATH)
       #print("Norm", os.path.normpath(BASE_PATH))
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #print("DATA", self.data)
        sections = self.data.split()
        self.decoded = self.data.decode()
        #print('DECODED\n', decoded)
        self.decoded = self.decoded.split()
        #print("1", decoded[1])
       
        if self.decoded[0] == 'GET':
            self.try_get()
        else:
            self.error_405()

        self.request.sendall(bytearray("OK",'utf-8'))

    def try_get(self):
        print("The Path is", self.decoded[1])
        path = self.decoded[1]
        
        if path == '/deep':
            path = BASE_PATH+'/deep/'
            #print("checking1..", os.path.isfile(path))
            self.http_status_code = 200
        elif path[-1] == '/':
            path = BASE_PATH+path+'index.html'
            #print("checking2..", os.path.isfile(path))
            self.http_status_code = 200
        elif path[-4:] == '.css':
            path = BASE_PATH+path
            #print("checking3..", os.path.isfile(path))
            self.mime_type = 'text/css'
            self.http_status_code = 200
        elif path[-5:] == '.html':
            path = BASE_PATH+path
            #print("checking4..", os.path.isfile(path))
            self.mime_type = 'text/html'
            self.http_status_code = 200
        try:
            file = open(path, "r")
            content = file.read()
        except Exception as e:
            
            self.http_status_code = 404
            print("error 404 not found")
        
        #pass

    def error_405(self):
        self.http_status_code = 405
        #self.result = self.decoded[2]+self.http_status_code+'\n'+self.decoded[3]+
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
