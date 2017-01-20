#  coding: utf-8 
import SocketServer
import shlex
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
class HTTPFile():
    def __init__(self):
        self.headers = [""]
        self.found = False
        self.file = ""

    def __str__(self):
        s = ""
        for l in self.headers:
            s += l + "\r\n"

        s += "\r\n"

        if self.found:
            with open(self.file, "rb") as f:
                s += f.read()

        return s


class RegularFile(HTTPFile):
    def __init__(self, path):
        self.headers = ["HTTP/1.1 200 OK", "Content-Type: text/plain"]
        self.file = path
        self.found = True

class CSSFile(RegularFile):
    def __init__(self, path):
        RegularFile.__init__(self, path)
        self.headers[1] = "Content-Type: text/css"

class HTMLFile(RegularFile):
    def __init__(self, path):
        RegularFile.__init__(self, path)
        self.headers[1] = "Content-Type: text/html"

class NoFile(HTTPFile):
    def __init__(self):
        HTTPFile.__init__(self)
        self.headers = ["HTTP/1.1 404 Not FOUND!"]

class InvalidMethod(HTTPFile):
    def __init__(self):
        self.headers = ["HTTP/1.1 405 Method Not Allowed"]

class FileFactory():
    location_prefix = "www/"

    def __init__(self):
        self.www_dir = os.path.join(os.getcwd(), self.location_prefix)
        self.types = {"css": CSSFile, "html": HTMLFile}

    def get_file(self, data):
        command = self.get_keys(data)
        path = self.get_path(command)
        if command['command'].upper() != "GET":
            return InvalidMethod()
        if self.www_dir not in os.path.abspath(path) or not os.path.isfile(path):
            return NoFile()
        else:
            extension = path.split(".")[-1].lower()
            if extension in self.types.keys():
                return self.types[extension](path)
            else:
                return RegularFile(path)

    def get_path(self, command):
        path = os.path.join(self.location_prefix, command['path'].lstrip("/"))
        if path[-1] == "/":
            path += "index.html"
        return path

    def get_keys(self, command):
        command = shlex.split(command[0])
        keys = {}
        keys['command'] = command[0]
        keys['path'] = command[1]
        keys['http'] = command[2]
        for i in range(1, len(command)):
            command[i].split(":")
            keys[command[0].strip()] = command[1].strip()

        return keys

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip().split("\r\n")
        filefactory = FileFactory()
        obj = filefactory.get_file(self.data)
        self.request.sendall(str(obj))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
