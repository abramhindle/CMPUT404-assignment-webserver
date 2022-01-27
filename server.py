#  coding: utf-8 
import socketserver
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2022 Lidia Ataupillco-Ramos
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

# declare constant variables
PROTOCOL = 'HTTP/1.1'
OK_STATUS_CODE = '200 OK'
N_ALLOW_METH = '405 Method Not Allowed'
HTML_FILE_NAME = 'index.html'
REDIR_STATUS_CODE = '301 Moved Permanently'
NFOUND_STATUS_CODE = '404 Not Found'
HTML_MIME_TYPE = 'text/html'
CSS_MIME_TYPE = 'text/css'

# construct the header string from a dictionary
def construct_header_str(headers):
    header_str = ''
    for header in headers:
        header_str += f'{header}:{headers[header]}\r\n'
    
    header_str += '\r\n'
    return header_str.encode('utf-8')

# obtains the binary object of the file requested using the uri
def get_bbody(uri):
    file_path = ''
    if uri.endswith('/') or uri.endswith('/index.html'):
        # locate path for the html file
        file_path = f'{uri}' if uri.endswith('/index.html') else f'{uri}{HTML_FILE_NAME}'
    elif uri.endswith('.css'):
        file_path = f'{uri}'
    else:
        # Location issues
        return f'<html>File moved</html>'.encode('utf-8')

    # read corresponding file
    try:
        file_obj = open(f"www{file_path}", 'r')
    except:
        # raises an error so that the caller function handles the 404 error
        raise FileNotFoundError
    
    # encode file into binary
    bbody = file_obj.read().encode('utf-8')
    return bbody

class MyWebServer(socketserver.BaseRequestHandler):
    def handle_requests(self, request_info):
        # obtain main information not part of the body
        main = request_info[0].split()

        # obtain method
        method = main[0]
        uri = main[1]
        raw_req_headers = main[2]

        req_headers = {}
        # are we using request headers?
        # for val in raw_req_headers[1:]:
        #     t = val.split(": ")
        #     parsed_info[t[0]] = t[1]

        return method, uri, req_headers
    
    # method that sends the response to the client
    def send_response(self, request, bbody, status, headers):
        # send request line
        request_line = f'{PROTOCOL} {status}\r\n'.encode('utf-8')
        request.sendall(request_line)
        
        # send headers
        header_str = construct_header_str(headers)
        request.sendall(header_str)

        # send body 
        request.sendall(bbody + b'\n')

    def handle(self):
        self.data = self.request.recv(1024).strip()

        request_info = self.data.decode().split("\r\n")

        print ("Got a request of: %s\n" % self.data)
        method, uri, req_headers = self.handle_requests(request_info)

        # initialize the encoded body
        bbody = b''
        # any header types that are not content-type, content-length or connection
        extra_headers = {}

        if method == 'GET':
            try:
                bbody = get_bbody(uri)
            except FileNotFoundError:
                # send 404 error to the client: no found message
                bbody = f'{uri.capitalize()} path not found.'.encode('utf-8')
                
                # generate headers
                headers = {
                    'Content-Type': 'text/html; charset=utf-8',
                    'Content-Length': f'{len(bbody)}',
                    'connection': 'close'
                }

                # send message
                self.send_response(self.request, bbody, NFOUND_STATUS_CODE, headers)
                self.finish()
                return 

            if uri.endswith('.css'):
                content_type = CSS_MIME_TYPE
                status = OK_STATUS_CODE

            elif uri.endswith('/') or uri.endswith('/index.html'):
                content_type = HTML_MIME_TYPE
                status = OK_STATUS_CODE               
            else:
                # redirect
                content_type = HTML_MIME_TYPE
                status = REDIR_STATUS_CODE
                new_address = f'http://127.0.0.1:8080{uri}/'

                extra_headers = {
                    'Location': f'{new_address}'
                }
        else:
            # Response for method not handled
            # create message
            bbody = f'<html>Method {method} not allowed. You can only make GET requests.</html>\n'.encode('utf-8')
            content_type = HTML_MIME_TYPE
            status = N_ALLOW_METH

        # generate headers
        headers = {
            'Content-Type': f'{content_type}',
            'Content-Length': f'{len(bbody)}',
            'connection': 'close'
        }

        # add the extra headers
        headers.update(extra_headers)

        # send message
        self.send_response(self.request, bbody, status, headers)
        self.finish()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
