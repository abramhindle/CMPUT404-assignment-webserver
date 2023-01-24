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
    extension_code = {
        'NOTHING': None,
        'INDEX_PAGE': 'index.html',
        'NOT_FOUND': '404'
    }

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        # Now that we have the response. We need to parse it. parse_request
        # already decodes the data.
        request_is_good = self.parse_request(self.data)
        print(self.extension)
        if request_is_good == -1:   # handling any POST/PUT/DELETE request
            print("Something")
            self.request.sendall(bytearray(
                f"HTTP/1.1 405 METHOD NOT ALLOWED/r/nContent-Type: 'text/html'/r/nContent-Length: {len(f)}; encoding=utf-8/r/n/r/nThis works!", 'utf-8'))
            return
        elif self.extension == 'index.html':  # directed to index.html
            self.request.sendall(bytearray(
                f"HTTP/1.1 200 OK\r\ncontent-Type: text/html; encoding=utf-8\r\n\r\nThis works!", 'utf-8'))
            return
        elif self.extension == '404':
            self.request.sendall(bytearray(
                f"HTTP/1.1 404 NOT FOUND\r\ncontent-Type: text/html; encoding=utf-8\r\n\r\nThis works!", 'utf-8'))

    def parse_request(self, data):
        self.data = data.decode('utf-8')
        # Is the message anything other than GET?
        if self.data[:3] != 'GET':
            return -1

        self.extension = ''
        # There is no extension after base url
        if self.data[4:6] == '/ ':
            self.extension = None
        elif self.data[4:15] == '/index.html':  # requested for index.html
            self.extension = 'index.html'
        else:  # request is okay but cannot find the extension requested.
            self.extension = '404'
        return 1

        '''
        Content-Type': 'text/html; encoding=utf8'
        self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\n"))

        

        if self.data[:3] = "GET"
        f = open(index.html)
        f1 = f.read
        f.close
        self.request.sendall(bytearray(f"HTTP/1.1 200 OK/r/nContent/r/n/r/n{f1}", 'utf-8'))
        self.request.sendall(bytearray("HTTP", 'utf-8'))'''


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


file index.html
f = open("www/"+file)