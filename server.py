#  coding: utf-8 
import socketserver
import requests
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

# From https://www.tutorialspoint.com/http/http_responses.htm
class HTTPResponse:
    def __init__(self, status, content_type=None, message=None):
        self.status = status
        self.content_type = content_type
        self.message = message

    def status_line(self):
        return "HTTP/1.1 {self.status}\n".format(self=self)
        
    def content_lines(self):
        content_type = "Content-Type: text/{self.content_type}\r\n".format(self=self)
        content_length = "Content-Length: {}\n".format(len(self.message.encode()))
        return content_length + content_type

    def location_line(self):
        return "Location: {self.location}\n".format(self=self)

    def format_response(self):
        response = self.status_line()
        if(self.message):
            response += self.content_lines() + "\n" + self.message
        return response
        

class MyWebServer(socketserver.BaseRequestHandler):

    def handle_file(self, path):
        # From https://stackoverflow.com/questions/68477/send-file-using-post-from-a-python-script
        with open(path, 'r') as f:
            content_type = path.split(".")[1]
            return HTTPResponse("200 OK", content_type, f.read())

    def handle_request(self, page):
        # From https://docs.python.org/3/library/os.path.html
        path = os.path.abspath("www" + page)
        if (os.path.isdir(path)):
            if(page.endswith("/")):
                path += "/index.html"
            else:
                return HTTPResponse("301 Moved Permanently")
        # https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
        if(os.path.exists(path) and (os.path.abspath("www") in path)):
            return self.handle_file(path)
        else:
            print(path)
            return HTTPResponse("404 Not Found")
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        # From https://www.tutorialspoint.com/http/http_requests.htm
        method = self.data.split()[0]
        page = self.data.split()[1]
        if(method == 'GET'):
            r = self.handle_request(page)
        else:
            r = HTTPResponse("405 Method Not Allowed")
        self.response = r.format_response()
        self.send_response()
        
    def send_response(self):
        self.request.sendall(bytearray(self.response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()