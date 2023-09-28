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
NEWLINE = '\n'
CLOSE = 'close'

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #print("Path", BASE_PATH)
       #print("Norm", os.path.normpath(BASE_PATH))
        self.data = self.request.recv(1024).strip()
        #print(self.data)
        #print ("Got a request of: %s\n" % self.data)
        #print("DATA", self.data)
        sections = self.data.split()
        self.decoded = self.data.decode()
        #print('DECODED\n', decoded)
        self.decoded = self.decoded.split()
        #print("1", decoded[1])
        #print(self.decoded)
        if self.decoded[0] == 'GET':
           self.try_get()
        else:
            #print(self.decoded[0])
            self.error_405()
        #self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_type+NEWLINE+NEWLINE+self.content
        #print(sending)
        self.request.sendall(bytearray(self.sending, 'utf-8'))
        #self.request.sendall(bytearray("OK",'utf-8'))

    def try_get(self):
        #print("The Path is", self.decoded[1]+NEWLINE)
        self.path = self.decoded[1]
        #print("THE PATH", self.path)
        self.mime_type = ''
        if self.path == '/deep':
            self.path = BASE_PATH+self.path+'/'
            #print("checking1..", os.path.isfile(path))
            self.decoded[1] = '/deep/'
            #self.send_header('Location', self.decoded[1])
            self.http_status_code = 301 #moved permanenly!
            #Redirected! :) or 300?/307/8?
        elif self.path[-1] == '/':
            self.path = BASE_PATH+self.path+'index.html'
            self.mime_type = 'text/html'
            #print("checking2..", os.path.isfile(path))
            self.http_status_code = 200
            # Found! :)
        elif self.path[-4:] == '.css':
            self.path = BASE_PATH+self.path
            #print("checking3..", os.path.isfile(path))
            self.mime_type = 'text/css'
            self.http_status_code = 200
            #Found! :)
        elif self.path[-5:] == '.html':
            self.path = BASE_PATH+self.path
            #print("checking4..", os.path.isfile(path))
            self.mime_type = 'text/html'
            self.http_status_code = 200
        if self.path[-6:] == '/group':
            #Permission denied
            self.http_status_code = 404
            self.mime_type = ''
            self.content = ''
            self.error_404()
            return
        elif self.path == '/favicon.ico':
            self.mime_type = ''
            self.content = ''
            self.http_status_code = 200
            self.pass_200()
            return
        # print("The Path is", self.decoded[1]+NEWLINE)
        try:
            #print('trying', self.path)
            file = open(self.path, "r")
            self.content = file.read()
            #print(self.content)
            #print('success!')
            self.pass_200()
        except FileNotFoundError as e:
            #print("Path", self.path, "Has failed for some reason.")
            # try:
            #     print("Inside second try", self.path)
            #     self.path = self.path+'/'
            #     file.open(self.path, "r")
            #     self.content = file.read()
            #     print('success!')
            #     self.redirect_301()

            # except:
            #print("error 404 not found")
            self.error_404()
        except IsADirectoryError as e:
            #print("redirecting...")
            self.content = ''
            self.redirect_301()
            
                
                
        #return self.path
    
    def error_404(self):
        self.http_status_code = 404
        self.content = ''
        self.content_type = 'text/html'
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_type+NEWLINE+NEWLINE+self.content+NEWLINE+"Connection: "+CLOSE +NEWLINE
        

    def pass_200(self):
        self.http_status_code = 200
        if self.path[-4:] == '.css':
            self.path = BASE_PATH+self.path
            #print("checking3..", os.path.isfile(path))
            self.content_type = 'text/css'
            #Found! :)
        elif self.path[-5:] == '.html':
            self.path = BASE_PATH+self.path
            #print("checking4..", os.path.isfile(path))
            self.content_type = 'text/html'
        else:
            self.path = BASE_PATH+self.path
            self.content_type = 'text.html'

        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_type+NEWLINE+NEWLINE+self.content+NEWLINE+"Connection: "+CLOSE +NEWLINE
            

    def redirect_301(self):
        self.content_type = 'text/html'
        self.http_status_code = 301
        self.location = self.path
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Location'+self.location+NEWLINE+'Content-Type: '+self.content_type+NEWLINE+NEWLINE+self.content+NEWLINE+"Connection: "+CLOSE +NEWLINE



    def error_405(self):
        self.content = ''
        self.content_type = 'text/html'
        self.http_status_code = 405
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_type+NEWLINE+NEWLINE+self.content+NEWLINE+"Connection: "+CLOSE +NEWLINE
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
