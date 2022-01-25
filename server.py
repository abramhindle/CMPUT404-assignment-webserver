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

PROTOCOL = 'HTTP/1.1'
OK_STATUS_CODE = '200 OK'
N_ALLOW_METH = '405 Method Not Allowed'

class MyWebServer(socketserver.BaseRequestHandler):
    def handle_requests(self, request_info):
        # obtain request headers
        main = request_info[0].split()

        # obtain method
        method = main[0]
        uri = main[1]
        status = main[2]

        parsed_info = {}
        for val in request_info[1:]:
            t = val.split(": ")
            parsed_info[t[0]] = t[1]

        return method, uri, parsed_info
    
    def handle_get_res(self):
        pass

    def handle(self):
        print("address", self.client_address)
        self.data = self.request.recv(1024).strip()

        request_info = self.data.decode().split("\r\n")

        print ("Got a request of: %s\n" % self.data)
        method, uri, parsed_info = self.handle_requests(request_info)

        if method == 'GET':
            ok_request_line = f'{PROTOCOL} {OK_STATUS_CODE}\r\n'
            # read files
            # read html file
            if uri.endswith('.css'):
                self.request.sendall(bytearray(ok_request_line + f'content-Type: text/css; charset=utf-8\r\n' + f'content-Length: 48\r\n' + f'connection: close\r\n\r\n', 'utf-8'))
                css_obj = open("www/base.css", 'rb')
                self.request.sendall(css_obj.read() + b'\n')
            elif uri.endswith('/'):
                self.request.sendall(b'HTTP/1.1 200 OK\r\n' + b'content-Type: text/html; charset=utf-8\r\n' + b'content-Length: 471\r\n' + b'connection: close\r\n\r\n')
                file_obj = open("www/index.html", 'rb')
                self.request.sendall(file_obj.read() + b'\n')
        else:
            # method not handled
            nallow_request_line = f'{PROTOCOL} {N_ALLOW_METH}\r\n'
            self.request.sendall(bytearray(nallow_request_line, 'utf-8'))
            header_nallow_meth = 'Content-Type:text/plain\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'
            self.request.sendall(bytearray(header_nallow_meth, 'utf-8'))

        # CSS
        # self.request.sendall(b'HTTP/1.1 200 OK\r\n' + b'content-Type: text/css\r\n' + b'content-Length: 48\r\n' + b'Connection: keep-alive\r\n\r\n')
        # css_obj = open("www/base.css", 'rb')
        # self.request.sendall(css_obj.read())

        # self.request.sendall(bytearray(css_obj.read() + '\n','utf-8'))


        # root_html = bytearray(file_obj.read() + '\n','utf-8')

        ##### USE SENDFILE

        # send response
        self.request.sendall(b'HTTP/1.1 200 OK\r\n' + b'content-Type: text/html; charset=utf-8\r\n' + b'content-Length: 471\r\n\r\n')
        # self.request.sendall(b'\r\n\r\n')

        self.finish()
    
    def decode(self, data):
        return data.decode()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
