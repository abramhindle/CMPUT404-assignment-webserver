#  coding: utf-8
import socketserver
import os.path
from os import path

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

    # print ("directory exists:" + str(path.exists('www')))



    def handle404(self):
        pass

    def handle301(self, requestMethod):
        print("not correct /")
        return 1

    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestMethod = self.data.decode('utf-8')
        check405 = requestMethod.split(" ")[0]


        if(check405 != 'GET'):
            response = self.handle405(requestMethod)
        else:
            print("go ahead")
            check301 = requestMethod.split(" ")[2]
            print(check301)
            # if((check301[-1])!="/"):
            #     self.handle301(requestMethod)
            # else:
            #     print("correct address" + check301)
        self.request.sendall(bytearray("OK",'utf-8'))

    def handle405(self, request):
        print("not allowed")
        return 1





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
