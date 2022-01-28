#  coding: utf-8 
import socketserver
import os 
from datetime import datetime


# Copyright 2022 Della Humanita
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
        # self.request is the TCP socket connected to the client
        received = self.request.recv(1024).strip()

        # parse the request
        method, url = self.parse_request(received.decode('utf-8'))

        # Get a response 
        response = self.send_response(method, url)

        if response:
            self.request.sendall(bytearray(f'{response}', 'utf-8'))

    
    def parse_request(self, req):
        '''
            Parses the request from the client and returns the method and url

            Args:
                req (str): the request from the client 

            Returns:
                method (str): the method of the request (GET, POST, etc.)
                url (str): the url of the request to serve
        '''

        start, headers = req.split('\r\n', 1)
        method, url, protocol = start.split(' ')

        return method, url


    def get_content_type(self, filepath):
        '''
            Returns the content type of the filepath

            Args:
                filepath (str): the filepath of the file

            Returns:
                content_type (str): the content type, e.g. text/html
        '''
        if filepath.endswith('.html') or filepath.endswith('/'):
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

        return paths
            

    def get_date(self):
        '''
            Returns the current date and time

            Returns:
                date (str): the current date and time
        '''
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S')


    def read_file_from_dir(self, filepath):
        '''
            Reads the files from the directory

            Args:
                filepath (str): the path of the file

            Returns:
                body (str): The file contents 
        '''

        with open(filepath, 'r', encoding='utf-8') as f:
            body = f.read()

            return body


    def get_status_code(self, method, requested_url):
        '''
            Returns the status code for the request

            Args:
                method (str): the method of the request (GET, POST, etc.)

            Returns:
                status_code (int): the status code of the request
        '''
        
        # Handle GET request and get the correct status code 
        if method == 'GET':
            
            # check if the url exists in the path
            if self.url_exists(requested_url) or self.url_exists(requested_url + '/'):
                status_code = 200

                # if the url does not end with '/ and it is an html page, redirect it to the correct url
                if (not requested_url.endswith('/') and 
                    not (requested_url.endswith('.html') or requested_url.endswith('.css'))):
                    status_code = 301
            # if it does not exist in the path, return Not Found
            else:
                status_code = 404

        # Send 405 response otherwise 
        else:
            status_code = 405
        
        return status_code
    
    
    def get_statuses(self):
        '''
            Returns a dictionary of status codes

            Returns:
                status_dict (dict): Dictionary of status codes and their corresponding messages

        '''
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
                'description': 'The requested resource has been moved permanently'},
            405: {
                'message': 'Method Not Allowed',
                'description': 'The method specified in the Request-Line is not allowed for the resource identified by the Request-URI'
            }
        }
        return status_dict

    def get_html(self, code, status_data, new_url=None):
        '''
            Creates an HTML page for the appropriate status code

            Args:
                code (int): the status code of the request
                status_data (dict): the status code dictionary
                new_url (str): the new URL to redirect to for a 301 status code

            Returns:
                html_page (str): the formatted HTML page 
        '''

        html_data = status_data[code]

        anchor_elem = ''
        if new_url:
            anchor_elem = f'<a href="{new_url}">here</a>.'
            
        html_page = f'''<!DOCTYPE html>
                    <html>
                    <head>
                    <title>{code} {html_data['message']}</title>
                    <meta http-equiv="Content-Type"
                    content="text/html;charset=utf-8"/>
                    </head>
                    <body>
                        <h1>{code} {html_data['message']}</h1>
                        {html_data['description']}
                        {anchor_elem}
                    </body>
                    </html>
                    '''

        return html_page
    
    def build_header(self, status_code, url, redirect_url=None):
        '''
            Builds the header of the response. Currently missing the Content-Length 
            and Location fields, which will be updated accordingly.

            Args:
                status_code (int): the status code of the request
                url (str): the url of the request

            Returns:
                header (str): the starter header of the response
        '''
        status = f'HTTP/1.1 {status_code} {self.get_statuses()[status_code]["message"]}\r\n'
        date = 'Date: ' + self.get_date() + '\r\n'
        content_type = 'Content-Type: ' + self.get_content_type(url) + '\r\n'

        if status_code == 301:
            location = f'Location: {redirect_url}\r\n'

        header = status + date + content_type

        return header
    
    def url_exists(self, url):
        '''
            Checks if the url exists in the paths dictionary

            Args:
                url (str): the url of the request
            
            Returns:
                True if the url exists in the paths dictionary, False otherwise
        '''
        return url in self.get_paths().keys()

    def get_body(self, status_code, requested_url):
        '''
            Returns the body of the response

            Args:
                status_code (int): the status code of the request
                requested_url (str): the url of the request
            
            Returns:
                body (str): The file contents if it is a 200 status code, otherwise an HTML page 
                            for the appropriate status code
        '''
        
        # if code is 200, read the file 
        if status_code == 200:
            paths = self.get_paths()

            for url in paths.keys():
                if requested_url == url:
                    file_content = self.read_file_from_dir(paths[url])
                    return file_content

        # else, return the html page
        else:
            status_data = self.get_statuses()

            if status_code == 301: 
                new_url = requested_url + '/'
                file_content = self.get_html(301, status_data, new_url)
            else:
                file_content = self.get_html(status_code, status_data)

            return file_content

    def build_response(self, header, body):
        '''
            Appends the body to the header and adds CLRF to the end of the header

            Args:
                header (str): the header of the response
                body (str): the body of the response

            Returns:
                response (str): the complete response 
        '''

        content_length = f'Content-Length: {len(body)}\r\n'

        header += content_length + '\r\n'
        response = header + body

        return response

    def send_response(self, method, url):
        '''
            Retrieves the appropriate status code to create the header and body and 
            creates a response to the client.

            Args:
                method (str): the method of the request (GET, POST, etc.)
                url (str): the url of the request

            Returns:
                response (str): the complete response to the client
        '''


        # get the status code 
        status_code = self.get_status_code(method, url)

        # get the header 
        if status_code == 301:
            header = self.build_header(status_code, url, url + '/')
        else:
            header = self.build_header(status_code, url)

        # get the body
        body = self.get_body(status_code, url)

        response = self.build_response(header, body)

        return response


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
