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

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.redirect = False
        self.process_data()
        if self.action != b'GET':
            self.response((self.statu_codes("405") +"\n"))
            return

        if self.directory:
            try:
                result = self.open_file(self.directory)
                temp = self.directory.split('.')
                content_type = "Content-Type: text/%s;\r\n"%temp[1]
                if self.redirect:
                    self.response((self.statu_codes("301") + content_type +"\n"+ result))
                else:
                    self.response((self.statu_codes("200") + content_type +"\n"+ result))

            except Exception as e:
                #raise HTTPError(404, self.statu_codes("404"))

                #raise HTTPError(self.statu_codes("404"))
                self.response((self.statu_codes("404") +"\n"))

    def statu_codes(self,code):
        codes = {
                "200": " 200 OK\r\n",
                "301": " 301 Moved Permanently\r\n:",
                "404": " 404 Not Found\r\n",
                "405": " 405 Method Not Allowed\r\n"
                }
        return self.http_version + codes[code]

    def process_data(self):
        requirements = self.data.split(b'\r\n')
        self.find_directory(requirements[0])
        self.info_dict = {}
        for item in requirements:
            try:
                temp = item.split(b':')
                self.info_dict[temp[0]] = temp[1]
            except Exception:
                pass

    def find_directory(self, value):
        try:
            temp = value.split(b' ')
            self.action = temp[0]
            self.directory = temp[1].decode("utf-8")
            self.http_version = temp[2].decode("utf-8")
            dir_temp = self.directory.split('/')
            if self.directory[-1] == '/' and "." not in dir_temp[-1]:
                self.directory += "index.html"
            elif self.directory[-1] != '/' and "." not in dir_temp[-1]:
                self.redirect = True
                self.directory += "/index.html"
            self.directory = self.directory[1:]
        except Exception as e:
            pass

    def open_file(self, filename):
        filename = "./www/" + filename
        f = open(filename, "r")
        return f.read()

    def response(self, value):
        self.request.sendall(bytearray(value,'utf-8'))





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
