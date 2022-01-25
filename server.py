#  coding: utf-8 
import socketserver
import os 
from datetime import datetime
import re
import sys

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

        # self.request is the TCP socket connected to the client
        received = self.request.recv(1024).strip()

        response = None
        try:
            # Parse the request from the client
            content_type, data = self.parse_request(received.decode('utf-8'))
            

            if content_type and data:
                response = self.do_GET(200, content_type, data)
                
            else:
                raise Exception
            
        except Exception as e:
            print('[ERROR]', e)
            self.handle_error()
            
        finally:
            if response:
                self.request.sendall(bytearray(f'{response}', 'utf-8'))
                print("Response:", response)

            print("Finished processing request.\n", '='*50)
    
    def parse_request(self, req):
        start, headers = req.split('\r\n', 1)
        method, url, protocol = start.split(' ')
        
        # Handle GET request
        if method == 'GET':
            try:
                if url == '/':
                    return 'text/html', self.read_file_from_dir('/index.html')

                css_regexpr = re.search('.\.css$', url)
                if css_regexpr is not None:
                    return 'text/css', self.read_file_from_dir(url)
            
            except Exception as e:
                print('[ERROR]', e)
                self.handle_error()

        else:
            self.handle_error()
            

    def get_date(self):
        '''
            Returns the current date and time
        '''
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S')


    def read_file_from_dir(self, url):
        '''
            Reads the files from the directory
        '''
        directory = 'www'
        
        filename = url[1:]

        for file in os.listdir(directory):
            if file == filename:
                path = directory + url
                with open(path, 'r', encoding='utf-8') as f:
                    body = f.read()

                    return body

    def do_GET(self, status_code, content_type, body):
        '''
            Returns the response to the client

        '''

        status = f'HTTP/1.1 {status_code} OK\r\n'
        date = 'Date: ' + self.get_date() + '\r\n'
        content_type = 'Content-Type: ' + content_type + '\r\n'
        content_len = 'Content-Length: ' + str(len(body)) + '\r\n'     

        header = status + date + content_type + content_len + '\r\n'
        
        
        return header + body


    def handle_error(self):
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))
        sys.exit()


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
