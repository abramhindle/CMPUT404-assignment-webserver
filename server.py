#  coding: utf-8 
import socketserver
import os 
from datetime import datetime

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
        '''
            Main function for handling a single request

        '''

        print("Starting server connection...")
        self.directory = 'www/'

        # Handle get request 
        try:
            # Get index.html 
            main_index = self.read_file_from_dir('index.html')

            www_index = self.do_GET(200, 'text/html', main_index)

            # Get base.css
            # main_css = self.read_file_from_dir('base.css')
            # # Get files in deep dir 
            # deep_index = self.read_file_from_dir('deep/index.html')
            # deep_css = self.read_file_from_dir('deep/base.css')

            # # Send the responses 
            
            # # www_css = self.do_GET(200, 'text/css', main_css, 'Link: <www/base.css>;rel=stylesheet\r\n\r\n')
            # # self.request.sendall(bytearray(f'{www_css}', 'utf-8'))

            # www_deep_index = self.do_GET(200, 'text/html', deep_index)
            # self.request.sendall(bytearray(f'{www_deep_index}', 'utf-8'))
            # print('Sent deep/index.html')
            # www_deep_css = self.do_GET(200, 'text/css', deep_css)
            
        except Exception as e:
            print('[ERROR]', e)
            self.handle_error()

        finally:
            # self.request.sendall(bytearray(f'{www_index}', 'utf-8'))
            self.request.sendall(bytearray(f'{www_index}', 'utf-8'))
            print('Sent index.html')
            print("Closing server connection...")
    
    def get_date(self):
        '''
            Returns the current date and time
        '''
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

    def read_file_from_dir(self, filename):
        '''
            Reads the html file 
        '''

        for file in os.listdir(self.directory):
            if file == filename:
                path = self.directory + file
                with open(path, 'r', encoding='utf-8') as f:
                    body = f.read()

                    return body

    def do_GET(self, status_code, content_type, body, other=None):
        status = f'HTTP/1.1 {status_code} OK\r\n'
        date = 'Date: ' + self.get_date() + '\r\n'
        content_type = 'Content-Type: ' + content_type + '\r\n'
        content_len = 'Content-Length: ' + str(len(body)) + '\r\n'     

        if other:
            return status + date + content_type + content_len + other + body
        
        return status + date + content_type + content_len + body


    def handle_error(self):
        response = 'HTTP/1.1 404 Not Found\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))


    #TODO: close connection if you don't want to keep reading requests
    #TODO: store a dictionary of all paths if it exists in the directory

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
