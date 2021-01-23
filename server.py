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

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        # get the request command
        req = self.parseRequest(self.data.decode('utf-8'))

        # get response and send
        if req:
            response = self.createResponse(req)
            self.request.sendall(response.encode())

    def createResponse(self, req):
        reqRoot = "./www"
        if req[0] == 'GET':
            reqURI = req[1]

            # prevent path getting out of www
            # for non-free-tests: test_get_group
            directories = reqURI.split("/")
            # print(reqURI, directories)
            level = 0
            for d in directories:
                if d != "..":  # go to folder
                    level += 1
                elif d == "..":  # go back
                    level -= 1
                if level < 0:  # out
                    return self.pageNotFound()

            reqPath = reqRoot + reqURI

            if reqURI[-1] != '/':
                # Must use 301 to correct paths such as http://127.0.0.1:8080/deep to http://127.0.0.1:8080/deep/ (path ending)
                if os.path.isdir(reqPath):
                    reqPath += '/'
                    return self.movedPermanently(reqURI + '/')
            # print("1", reqPath)
            if not os.path.isfile(reqPath):
                # The webserver can return index.html from directories (paths that end in /)
                if reqPath[-1] == '/':
                    reqPath += "index.html"
                else:  # The webserver can server 404 errors for paths not found
                    return self.pageNotFound()
            # print("3", reqPath)

            if not os.path.exists(reqPath):
                # print('not a exist path')
                return self.pageNotFound()

            # open file
            try:
                with open(reqPath, 'r') as f:
                    body = f.read()
            except:
                # print("Invalid file path")
                return self.pageNotFound()

            # content type
            (root, ext) = os.path.splitext(reqPath)
            if ext == ".css":
                mimeType = "text/css"
            else:
                mimeType = "text/html"

            # create header
            header = "HTTP/1.1 200 OK\r\n"
            cache = "cache-control: no-cache\r\n"
            contentType = "content-type: {};charset=UTF-8\r\n".format(
                mimeType)
            contentLen = "content-length: {}\r\n\n".format(len(body))
            # create response
            response = header + cache + contentType + contentLen + body
            return response
        else:
            # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
            return self.methodNotAllowed()

    def methodNotAllowed(self):
        # create response
        # The server MUST generate an Allow header field in a 405 response containing a list of the target resource's currently supported methods.
        header = "HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\n"
        with open('./www/405.html', 'r') as f:
            body = f.read()
        response = header + body
        return response

    def pageNotFound(self):
        # create response
        with open('./www/404.html', 'r') as f:
            body = f.read()
        # create header
        header = "HTTP/1.1 404 File not found\r\n"
        response = header + body
        return response

    def movedPermanently(self, location):
        # print("301", location)
        # create header
        header = "HTTP/1.1 301 Moved Permanently\r\n"
        response = header + "Location: "+location+"\r\n\n"
        # self.request.sendall(response.encode())
        return response

    def parseRequest(self, req):
        """
        return a parsed request
        """
        req = req.strip().split('\n')
        reqHTTP = req[0]  # GET / HTTP/1.1
        parts = reqHTTP.split(' ')
        if len(parts) != 3:
            return
        cmd = parts[0]
        path = parts[1]
        return (cmd, path)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
