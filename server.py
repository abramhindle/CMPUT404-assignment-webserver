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


def getFile(data):
    return data[1].decode("utf-8")


def isRequestValid(data):
    return len(data) > 2  # Empty request


def isMethodAllowed(data):
    return getRequestType(data) in ["GET"]  # Can extend this for other methods


# TODO: Refactor
def is404(filePath):
    return not os.path.exists(filePath)


def is301(reqFile):
    # Check for just / specification
    if reqFile[-1] == "/":
        return False
    if os.path.exists(reqFile) and not os.path.isfile(reqFile):
        return True


def getErrorResponse(code):
    statusCodes = {
        "405": "405 - Method Not Allowed",
        "301": "Moved Permanently",
        "404": "Oops, wrong page! We don't have it!",
    }
    errorMessage = "<p1>{}</p1>"
    if code == "405":
        errorMessage = errorMessage.format(statusCodes[code])
        errorMessageLength = len(errorMessage.encode("utf-8"))
        response = (
            "HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\nContent-length:"
            + str(errorMessageLength)
            + "\r\nContent-Type: text/html\r\n\r\n"
            + errorMessage
        )
        return response
    if code == "301":
        errorMessage = statusCodes[code]
        errorMessageLength = len(errorMessage.encode("utf-8"))
        response = (
            "HTTP/1.1 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080/deep/\r\n"
            + "\r\nConnection: close\r\n\r\n"
        )
        return response
    if code == "404":
        errorMessage = errorMessage.format(statusCodes[code])
        errorMessageLength = len(errorMessage.encode("utf-8"))
        response = (
            "HTTP/1.1 404 Page Not Found\r\nContent-length:"
            + str(errorMessageLength)
            + "\r\nContent-type: text/html\r\n\r\n"
            + errorMessage
        )
        return response


def processGET(data):
    renderFile = "www" + getFile(data)
    response = ""
    if renderFile[-1] == "/":
        renderFile += "index.html"
    else:
        if is301(renderFile):
            response = getErrorResponse("301")
            return response
    try:
        fileObj = open(renderFile, "r").read().encode("utf-8")
        contentlength = str(len(fileObj))
        fileObj = fileObj.decode("utf-8")
        if ".html" in renderFile:
            response = (
                "HTTP/1.1 200 OK\r\nContent-length:" + contentlength + "\r\nContent-Type: text/html\r\n\r\n" + fileObj
            )
        elif ".css" in renderFile:
            response = (
                "HTTP/1.1 200 OK\r\nContent-length:" + contentlength + "\r\nContent-Type: text/css\r\n\r\n" + fileObj
            )
        else:
            # Not serving any file other than html or css as per specs
            return getErrorResponse("404")
        return response
    except:
        if is404(renderFile):
            return getErrorResponse("404")


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.split()

        if not isRequestValid(self.data):
            return
        if not isMethodAllowed(self.data):
            errorMessage = getErrorResponse("405")
            self.request.sendall(bytearray(errorMessage, "utf-8"))
            return

        # Actually handling GET now
        if isMethodAllowed(self.data):
            answer = processGET(self.data)
            self.request.sendall(bytearray(answer, "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
