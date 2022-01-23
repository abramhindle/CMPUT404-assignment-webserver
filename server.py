#  coding: utf-8 
import socketserver
import os 
import codecs 

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
        print("Starting server connection...")
        self.directory = 'www/'

        index_text = self.do_GET()
        # index_text = ''

        self.request.sendall(bytearray(f'200 OK\n{index_text}', 'utf-8'))

    def do_GET(self):
        for file in os.listdir(self.directory):
            if file == 'index.html':
                path = self.directory + file
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    return text 
    

    def handle_error(self):
        self.request.sendall(bytearray("404 Not Found", 'utf-8'))


    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
