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

    OKSTATUS = "HTTP/1.1 200 OK\r\n"
    MOVEDSTATUS = "HTTP/1.1 301 Moved Permanently\r\n"
    NOTFOUNDSTATUS = "HTTP/1.1 404 Not Found\r\n"
    NOTALLOWEDSTATUS = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    
    def splitRequest(self, requestStr):
        # get the request method
        splitRequest = str(requestStr).split("b'")
        requestSplitBySpace = splitRequest[1].split(" ")
        # print(requestSplitBySpace)
        #requestMethod = requestSplitBySpace[0]
        return requestSplitBySpace
    

    def checkPath(self, path):
        print(os.path.exists(path))
        return os.path.exists(path)
    

    def readFileContents(self, path):
        
        file = open(path, "r")
        while True:
            bytesRead = file.read()
            print(bytesRead)
            if not bytesRead:
                break
        return bytearray(bytesRead, 'utf-8')
            

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        # get the request method
        splitRequest = self.splitRequest(self.data)
        requestMethod = splitRequest[0]
        print(splitRequest)

        # check for get request
        if requestMethod == "GET":
            # print(requestMethod)

            
            # get the file name
            filename = str(splitRequest[1])

            # check for a valid path
            if (self.checkPath("./www" + filename)):
                path = "./www" + filename

                # if root directory then redirect to index.html
                if (path.endswith("/") and self.checkPath(path + "index.html")):
                    path += "index.html"
                
                if (path.endswith(".css")):
                    contentType = "css"
                elif (path.endswith(".html")):
                    contentType = "html"
                
                fileContents = self.readFileContents(path)
                # print(os.path.getsize("./www"+filename))
            
                self.request.sendall(bytearray(self.OKSTATUS + "Content-Type: text/"+contentType+"\r\n\r\n" + str(fileContents),'utf-8'))
            else:
                self.request.sendall(bytearray(self.NOTFOUNDSTATUS,'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
