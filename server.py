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


class MyWebServer(socketserver.BaseRequestHandler):
    extension_code = {
        'NOTHING': None,
        'INDEX_PAGE': 'index.html',
        'NOT_FOUND': '404'
    }
    SPACE = '\r\n'
    END = '\r\n\r\n'
    NOT_OKAY = -1
    OKAY = 1

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        # Now that we have the response. We need to parse it. parse_request
        # already decodes the data.
        request_is_good = self.parse_request(self.data)

        if request_is_good == self.NOT_OKAY:   # handling any POST/PUT/DELETE request
            self.request.sendall(bytearray(
                f"HTTP/1.1 405 METHOD NOT ALLOWED{self.SPACE}Content-Type: 'text/html'{self.SPACE}Content-Length: 42{self.SPACE} encoding=utf-8{self.END}405 METHOD NOT ALLOWED", 'utf-8'))
            return

        elif self.extension == 'index.html':  # directed to default index.html
            self.serve_default_index()
            return

        elif self.extension == 'deep_index.html':
            self.serve_deep_index()
            return

        elif self.extension == 'base.css':
            self.serve_default_css()
            return

        elif self.extension == 'hardcode_index.html':
            self.serve_hardcode_index()
            return

        elif self.extension == 'hardcode_deep_index.html':
            self.serve_hardcode_deep_index()
            return

        elif self.parse_redirect() == 1:
            self.serve_redirect(1)
            return

        elif self.extension == '404':
            self.request.sendall(bytearray(
                f"HTTP/1.1 404 NOT FOUND\r\ncontent-Type: text/html; encoding=utf-8\r\n\r\nThis works!", 'utf-8'))
            return

    def parse_request(self, data):
        self.data = data.decode('utf-8')
        # Is the message anything other than GET?
        if self.data[:3] != 'GET':
            return -1

        self.extension = ''
        # If root or directly requesting index.html
        if self.parse_request_default_html():
            self.extension = 'index.html'
        elif self.parse_request_deep_html():
            self.extension = 'deep_index.html'
        elif self.parse_request_default_css():
            self.extension = 'base.css'
        elif self.parse_request_hardcode_html():
            self.extension = 'hardcode_index.html'
        elif self.parse_request_hardcode_deep_html():
            self.extension = 'hardcode_deep_index.html'

        # elif self.data[]

        else:  # request is okay but cannot find the extension requested.
            self.extension = '404'
        return 1

    """
    Parse the request path methods. ---------------------------------
    """

    def parse_request_default_html(self):
        if self.data[4:6] == '/ ' \
                or self.data[4:17] == '/index.html/ ' \
                or self.data[4:16] == '/index.html ':
            return True
        return False

    def parse_request_deep_html(self):
        end = self.data.find("HTTP")
        if self.data[4:end] == '/deep/ ' \
                or self.data[4:end] == '/deep/index.html '\
                or self.data[4:end] == '/deep/index.html/ ':
            return True
        return False

    def parse_request_hardcode_html(self):
        end = self.data.find("HTTP")
        end = end - 1
        if self.data[4:end] == '/hardcode/'\
                or self.data[4:end] == '/hardcode/index.html'\
                or self.data[4:end] == '/hardcode/index.html/':
            return True
        return False

    def parse_request_hardcode_deep_html(self):
        end = self.data.find("HTTP")
        end = end - 1
        if self.data[4:end] == '/hardcode/deep/'\
            or self.data[4:end] == '/hardcode/deep/index.html'\
                or self.data[4:end] == '/hardcode/deep/index.html/':
            return True
        return False

    def parse_redirect(self):
        end = self.data.find("HTTP")
        end = end - 1
        if self.data[4:end] == '/deep':
            return 1

    def parse_request_default_css(self):
        end = self.data.find("HTTP")
        if self.data[4:end] == '/base.css ' \
                or self.data[4:end] == '/base.css/ ':
            return True
        return False

    """
    Serve the page methods. ----------------------------------------
    """

    def serve_default_css(self):
        with open(os.getcwd() + "/www/base.css", 'r') as file:
            f_holder = file.read()
            f_holder = f_holder.replace('\n', '')
        self.request.sendall(bytearray(
            f"HTTP/1.1 200 OK{self.SPACE}Content-Type: text/css{self.SPACE}{self.END}{f_holder}", 'utf-8'))

    def serve_redirect(self, value):
        if value == 1:
            self.request.sendall(bytearray(
                f"HTTP/1.1 301 MOVED PERMANENTLY{self.SPACE}Location: http://127.0.0.1:8080/deep/{self.SPACE}{self.END}", 'utf-8'))

    def serve_hardcode_deep_index(self):
        with open(os.getcwd() + "/www/hardcode/deep/index.html", 'r') as file:
            f_holder = file.read()
            f_holder = f_holder.replace('\n', '')
        self.request.sendall(bytearray(
            f"HTTP/1.1 200 OK{self.SPACE}Content-Type: text/html{self.SPACE}{self.END}{f_holder}", 'utf-8'))

    def serve_deep_index(self):
        with open(os.getcwd() + "/www/deep/index.html", 'r') as file:
            f_holder = file.read()
            f_holder = f_holder.replace('\n', '')
        self.request.sendall(bytearray(
            f"HTTP/1.1 200 OK{self.SPACE}Content-Type: text/html{self.SPACE}{self.END}{f_holder}", 'utf-8'))

    def serve_default_index(self):
        with open(os.getcwd() + "/www/index.html", 'r') as file:
            f_holder = file.read()
            f_holder = f_holder.replace('\n', '')
        self.request.sendall(bytearray(
            f"HTTP/1.1 200 OK{self.SPACE}Content-Type: text/html{self.SPACE}{self.END}{f_holder}", 'utf-8'))

    def serve_hardcode_index(self):
        with open(os.getcwd() + "/www/hardcode/index.html", 'r') as file:
            f_holder = file.read()
            f_holder = f_holder.replace('\n', '')
        self.request.sendall(bytearray(
            f"HTTP/1.1 200 OK{self.SPACE}Content-Type: text/html{self.SPACE}{self.END}{f_holder}", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
