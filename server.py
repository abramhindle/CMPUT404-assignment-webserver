#  coding: utf-8 
from base64 import urlsafe_b64encode
import socketserver
import os 
from datetime import datetime
import re
import sys

import requests

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
        '''
            Main function for handling a single request

        '''
        print("Starting server connection...")

        # self.request is the TCP socket connected to the client
        received = self.request.recv(1024).strip()

        # parse the request
        method, url = self.parse_request(received.decode('utf-8'))

        response = None
        try:

            # Handle GET request
            if method == 'GET':
                print('Handling GET request...')
                success, content_type, data = self.handle_GET(url)

                if success:
                    response = self.do_GET(200, content_type, data)
                
                else:
                    print('Failed to GET body.')
                    raise Exception
            else:
                # TODO: send response for other methods ()
                print('Method not supported.')
                pass
            
        except Exception as e:
            print('[ERROR]', e)
            self.handle_error()
            
        finally:
            
            # refactored_response = self.build_response(method, url)

            if response:
                self.request.sendall(bytearray(f'{response}', 'utf-8'))
                # print("Response:", response)

            print("Finished processing request.\n", '='*50)

    
    def parse_request(self, req):
        '''
            Parses the request from the client and returns the method and url 

            Returns:
                method: the method of the request (GET, POST, etc.)
                url: the url of the request to serve
        '''

        start, headers = req.split('\r\n', 1)
        method, url, protocol = start.split(' ')

        return method, url

    def handle_GET(self, req_url):
        '''
            Takes the URL from the request header and sets the content-type and body

            Returns:
                success:    True if the request was successful, False otherwise
                content_type:   the content type of the response (text/html, text/css, etc.)
                body:   the body of the response

        '''
        
        paths = self.get_paths()

        for url in paths.keys():
            if req_url == url:
                file_content = self.read_file_from_dir(paths[url])
                content_type = self.get_content_type(paths[url])

                print('Content-Type:', content_type)
                print('File Content:', file_content)

                if file_content and content_type:
                    return (1, content_type, file_content)


        return (0, None, None)

    def get_content_type(self, filepath):
        '''
            Returns the content type of the filepath
        '''
        if filepath.endswith('.html'):
            return 'text/html'
        elif filepath.endswith('.css'):
            return 'text/css'
        else:
            return 'application/octet-stream'


        
    def get_paths(self):
        '''
            Create a dictionary of paths and their corresponding files. 
            Currently only works for the root directory and 1 nested folder.

            Returns
                paths   (dict)   : Key is the filepath and the value is the URL
        '''

        # dictionary of {filepath: set(urls)}
        paths = {}

        root = 'www/'

        # iterate through each file in www directory
        with os.scandir(root) as entries:
            for entry in entries:
                filepath = root  # start with the root path
                url = '/' # build url 

                # check if is a file or a directory
                # if it is a file, make the url and the filepath
                if entry.is_file():

                    filepath += entry.name
                    url += entry.name

                    # add to paths dictionary
                    paths[url] = filepath

                    # Special case to include '/' urls for index.html   
                    if entry.name == 'index.html':
                        paths['/'] = filepath
                
                # otherwise it is a directory
                else:
                    # iterate through each file in the nested directory 
                    with os.scandir(entry) as nested_entries:
                        for nested_entry in nested_entries:
                            # create their corresponding paths and urls
                            filepath = root + entry.name + '/' + nested_entry.name
                            url = '/' + entry.name + '/' + nested_entry.name

                            # add to paths dictionary
                            paths[url] = filepath

                            # Special case to include '/' urls for index.html       
                            if nested_entry.name == 'index.html':
                                paths['/' + entry.name + '/'] = filepath

        # for key, value in paths.items():
        #     print(f'{key}: {value}')

        return paths
            

    def get_date(self):
        '''
            Returns the current date and time
        '''
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S')


    def read_file_from_dir(self, filepath):
        '''
            Reads the files from the directory
        '''

        with open(filepath, 'r', encoding='utf-8') as f:
            body = f.read()

            return body

    def do_GET(self, status_code, content_type, body):
        '''
            Returns the response to the client

        '''

        status = f'HTTP/1.1 {status_code} OK\r\n'
        date = 'Date: ' + self.get_date() + '\r\n'
        content_type = 'Content-Type: ' + content_type + '\r\n'
        content_len = 'Content-Length: ' + str(len(body)) + '\r\n'     

        header = status + date + content_type + content_len + '\r\n'
        
        
        return header + body


    def handle_error(self):
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))
        sys.exit()

    
    def build_response(self, method, requested_url):
        statuses = self.get_statuses()
        paths = self.get_paths()
        corrected_url = None

        # Handle GET request and get the correct status code 
        if method == 'GET':
            status_code = 200
            # if url exists in paths, serve the file
            if not requested_url.endswith('/'):
                corrected_url = self.url_exists(requested_url + '/')
                if corrected_url:
                    status_code = 301 
                else:
                    status_code = 404           

        # Send 405 response otherwise 
        else:
            status_code = 405

        status_data = statuses[status_code]
        # Build the header
        header = self.build_header(status_code, requested_url)


        body = ''
        # Build the body 
        if status_code == 200:
            # read the file from the directory
            for url in paths.keys():
                if corrected_url == url:
                    body = self.read_file_from_dir(paths[url])

        else:
            if status_code == 301:
                body = self.get_html(status_data, corrected_url)
            else:
                body = self.get_html(status_data)

        # Append content length to header
        content_length = str(len(body))
        header += f'Content-Length: {content_length}\r\n\r\n'

        # Append the body to the header 
        response = header + body

        print('Response:', response)

        return response
    
    def get_statuses(self):
        status_dict = {
            200: {
                'message': 'OK',
                'description': 'The request has succeeded'
                },
            404: {
                'message': 'Not Found',
                'description': 'The requested resource could not be found.'
                },
            301: {
                'message':'Moved Permanently',
                'description': 'The requested resource has been moved permanently'}
        }
        return status_dict

    def get_html(self, status_data, new_url=None):

        code = status_data.keys()[0]

        anchor_elem = ''
        if new_url:
            anchor_elem = f'<a href="{new_url}">here</a>.'
            
        html_page = f'''
        <!DOCTYPE html>
        <html>
        <head>
        <title>{code} {status_data['message']}</title>
        <meta http-equiv="Content-Type"
        content="text/html;charset=utf-8"/>
        </head>
        <body>
            <h1>{code} {status_data['message']}</h1>
            {status_data['description']}
            {anchor_elem}
        </body>
        </html> '''

        return html_page
    
    def build_header(self, status_code, url):
        header = f'''
        HTTP/1.1 {status_code} {self.get_statuses()[status_code]['message']}\r\n
        Date: {self.get_date()}\r\n
        Content-Type: {self.get_content_type(url)}\r\n
        '''

        return header
    
    def url_exists(self, url):
        '''
            Checks if the url exists in the paths dictionary
        '''
        return url in self.get_paths().keys()

    def send_response(self):
        return 


    #TODO: close connection if you don't want to keep reading requests
    #TODO: store a dictionary of all paths if it exists in the directory

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
