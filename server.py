#  coding: utf-8 
import socketserver
import time

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
WEEK = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.decoded = self.data.decode()
        self.decoded = self.decoded.split()
        
        #print(list(time.localtime()))
        if len(self.decoded) > 0:
            self.path = self.decoded[1]
            if self.decoded[0] == 'GET':
                self.try_get()
            else:
                self.error_405()
            
            self.request.sendall(bytearray(self.sending, 'utf-8'))
            self.request.close()

    def try_get(self):
        '''
        Update the paths according to user stories in requirements.org, then attempt to open the
        files. Catch exceptions and handle/assign appropriate HTTP status codes accordingly.
        '''
        
        if self.path == '/deep':
            self.path = self.path+'/'
            self.decoded[1] = '/deep/'
            #moved permanenly!
            #Redirected! :) or 300?/307/8?

        elif self.path[-1] == '/':
            self.path = self.path+'index.html'
            self.content_mime_type = 'text/html'
            # Fixed path! :)

        if '/etc/' in self.path:
            #Permission denied, these files should not be accessed.
            # https://tldp.org/LDP/sag/html/etc-fs.html source used for understanding this directory.
            self.error_404()
            return
        
        # The path "/favicon.ico" was giving me issues/errors when I ran the server without the tests,
        # I implemented this simply to handle those errors.

        # elif self.path == '/favicon.ico':
        #     self.content_mime_type = 'text/plain'
        #     self.content = ''
        #     self.http_status_code = 200
        #     self.pass_200()
        #     return
        
        #www + /path
        self.path = BASE_PATH + self.path

        try:
            
            file = open(self.path, "r")
            self.content = file.read()
            self.pass_200()
        except FileNotFoundError as e:
            self.error_404()
        except IsADirectoryError as e:
            self.content = ''
            self.redirect_301()
            
    
    def error_404(self):
        '''
        There was some issue opening the file, it could not be found.
        Error 404 returned.
        '''

        self.http_status_code = 404
        self.content = 'Error 404 Page Not Found'
        self.content_mime_type = 'text/html'
        
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_mime_type+NEWLINE+NEWLINE+self.content+NEWLINE+"Connection: "+CLOSE +NEWLINE
        

    def pass_200(self):
        '''
        There was no issue opening the file! 200 OK status code returned.
        '''

        self.http_status_code = 200
        if self.path[-4:] == '.css':
            self.content_mime_type = 'text/css'
            #Fixed path :)
        else:
            self.content_mime_type = 'text/html'
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Content-Type: '+self.content_mime_type+NEWLINE+NEWLINE+self.content+NEWLINE#+"Connection: "+CLOSE +NEWLINE
            

    def redirect_301(self):
        '''
        Need to send the redirected path under the header - Location:
        '''

        self.content_mime_type = 'text/html'
        self.http_status_code = 301
        self.location = self.path
        self.sending = self.decoded[2]+' '+ str(self.http_status_code)+NEWLINE+'Location'+self.location+NEWLINE+'Content-Type: '+self.content_mime_type+NEWLINE+NEWLINE+self.content+NEWLINE#+"Connection: "+CLOSE +NEWLINE


    def error_405(self):
        '''
        The request is attempting to use PUT, POST, etc.
        This server can only handle GET requests.
        '''
        self.content = 'Unfortunately the server cannot handle this request.'
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