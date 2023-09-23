#  coding: utf-8 
import socketserver
import os
import mimetypes


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
        redirect = False
        self.data = self.request.recv(1024).strip()
        print ("\n\nGot a request of: %s" % self.data)
        # parse request
        method = self.data.split()[0].decode('utf-8')
        file_name = self.data.split()[1].decode('utf-8')
        file_path = os.path.abspath("www" + file_name)
        if os.path.exists(file_path) and os.path.isdir(file_path):
            if file_name[-1] != '/':
                file_name += '/'
                redirect = True
            else:
                file_name += 'index.html'

        print("File name: " + file_name)
        print("Method: " + method)
        
        if method == "GET":
            content = self.read_file(file_name)
            if content != None:
                if redirect:
                    print("301 Moved Permanently: "+ file_name)
                    self.send_response(301, "Moved Permanently", None, None, ("http://"+HOST+":"+str(PORT)+file_name))
                else:
                    print("200 OK")
                    self.send_response(200, "OK", content, mimetypes.guess_type(os.path.abspath("www" + file_name)))
            else:
                self.send_response(404, "File not found")
        else:
            self.send_response(405, "Method not allowed")
    
    def read_file(self, file_name):
        file_path = os.path.abspath("www" + file_name)
        if os.path.exists(file_path):
                print("File exists")
                f = open(file_path, 'rb')
                content = f.read()
                f.close()
                return content  
        else:
            print("File does not exist")
            return None

    def send_response(self, code, message, content=None, content_type=None, new_location=None):
        if code == 200:
            print("mime type: " + str(content_type))
            response = f"HTTP/1.1 {code} {message}\r\n"
            response += f"Content-Type: {content_type[0]}\r\n"
            response += f"Content-Length: {len(content)}\r\n"
            response += "\r\n"
            response += content.decode("utf-8")
            print("response:\n"+response)
            self.request.sendall(response.encode("utf-8"))
        elif code == 301:
            response = f"HTTP/1.1 {code} {message}\r\n"
            response += f"Location: {new_location}\r\n"
            response += "\r\n"
            self.request.sendall(response.encode("utf-8"))
        else:
            response = f"HTTP/1.1 {code} {message}\r\n"
            self.request.sendall(response.encode("utf-8"))
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
