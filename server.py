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

import os


def getRequestType(data):
    return data[0].decode("utf-8")


def isRequestValid(data):
    return len(data) > 2


def is405(data):
    return getRequestType(data) != "GET"


def is404(filePath):
    return os.path.exists(filePath)


def getErrorResponse(code):

    if code == "405":
        errorMessage = "<p1> 405 - Method Not Allowed</p1>"
        errorMessageLength = len(errorMessage.encode("utf-8"))
        response = (
            "HTTP/1.1 405 - Method Not Allowed\r\nAllow: GET\r\nContent-length:"
            + str(errorMessageLength)
            + "\r\nContent-Type: text/html\r\n\r\n"
            + errorMessage
        )
        print(response)
        return response


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.split()
        if not isRequestValid(self.data):
            return
        if is405(self.data):
            errorMessage = getErrorResponse("405")
            self.request.sendall(bytearray(errorMessage, "utf-8"))
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
