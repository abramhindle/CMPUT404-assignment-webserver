#  coding: utf-8
import socketserver
import os.path
import time
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
        request_string = self.data.decode('utf-8')
        check_status = request_string.split(" ")

        # create response handler
        http_response = self.check_405(check_status)
        if not http_response:
            http_response = self.check_404(check_status)
            if not http_response:
                http_response="working"
        self.request.sendall(bytearray(http_response,'utf-8')) # serving the response to the server

    def check_405(self, request):
        if(request[0]!="GET"):
            page = self.return_error_html("405 Method Not Allowed")
            return self.return_HTTP("405 Method Not Allowed", page)
        return False

    def check_404(self, request):
        # check validity of request url
        # send 404 if file doesn't exist in ./www
        # from stackoverflow answer by aghast https://stackoverflow.com/users/4029014/aghast
        # https://stackoverflow.com/questions/36142188/search-a-directory-including-all-subdirectories-that-may-or-may-not-exist-for
        parent = os.path.abspath("www")
        path_given = request[1]

        print(f"parent: {parent}")
        print(f"path: {path_given}")
        print(request[:2])

        if os.path.exists(parent + path_given):
            if path_given[-1] == "/":
                if "html" not in path_given:
                    newpath = parent + path_given + "index.html"
                else:
                    newpath = parent + path_given[:-1]
            else:
                newpath = parent + path_given

            print(newpath)
            fetch_page = open(newpath, "r")
            read_page = fetch_page.read()
            fetch_page.close()

            if "html" in newpath:
                mimetype = "text/html"
            elif "css" in newpath:
                mimetype = "text/css"
            return """HTTP/1.1 {}\r\nAllow: GET\r\nContent-Type: {}\r\nConnection: close\r\n\r\n{}""".format("200 OK",mimetype,read_page)
        return False



        #
        # for (dir,subdirs,files) in os.walk('www'):
        #     if given_path[1:] in subdirs:
        #         if given_path[-1] != "/":
        #             page = self.return_error_html(f"301 Moved Permanently\r\nLocation: {given_path}/\r\n")
        #             return self.return_HTTP(f"301 Moved Permanently\r\nLocation: http://localhost:8000{given_path}/\r\n",page)
        #
        #     if given_path[1:] in files:
        #         print(os.path.abspath(given_path))
        #         url = os.path.join('www',given_path)
        #         if "html" in given_path:
        #             mimetype = "text/html"
        #         elif "css" in given_path:
        #              mimetype = "text/css"
        #         fetch_page = open(url, "r")
        #         read_page = fetch_page.read()
        #         fetch_page.close()
        #         return """HTTP/1.1 {}\r\nAllow: GET\r\nContent-Type: {}\r\nConnection: close\r\n\r\n{}""".format("200 OK",mimetype,read_page)
        #

    def check_301(self, request):
        pass
    def check_200(self, request):
        pass

    def return_HTTP(self, status_code, page):
        http = """HTTP/1.1 {}\r\nAllow: GET\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n{}""".format(status_code,page)
        return http

    def return_error_html(self, status_code):
        page = """
        <!DOCTYPE html>
        <html>
        <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        </head>

        <body>
            <h1>{}</h1>
        </body>

        </html>
        """.format(status_code)
        return page



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
