#  coding: utf-8
import dataclasses
import enum
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
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Optional


class Method(enum.Enum):
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


@dataclass
class Request:
    method: Method
    target: str
    version: str
    headers: Dict[str, str]
    body: Optional[bytes]


@dataclass
class Response:
    version = "HTTP/1.1"
    status: int
    headers: Dict[str, str] = dataclasses.field(default_factory=dict)
    body: Optional[bytes] = None

    def serialize(self):
        return b"\r\n".join([
            f"{self.version} {self.status} {HTTPStatus(self.status).phrase}".encode(),
            *[f"{key}: {value}".encode() for key, value in self.headers.items()],
            b"" if self.body is None else self.body
        ])


class MyWebServer(socketserver.BaseRequestHandler):
    METHOD_NOT_ALLOWED_RESP = Response(405)
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.set_parsed_req()
        print(f"request: {self.parsed_req}")
        if self.parsed_req.method != Method.GET:
            self.request.sendall(self.METHOD_NOT_ALLOWED_RESP.serialize())
        else:
            self.parsed_req.target

    def set_parsed_req(self):
        meta, *body = self.data.split(b"\r\n\r\n")
        body = body[0] if body else None
        startline, *rest = meta.decode().split('\r\n')
        headers = {}
        for raw_header in rest:
            colon_idx = raw_header.find(":")
            #                 skip colon and whitesepace V
            headers[raw_header[:colon_idx]] = raw_header[colon_idx + 2:]
        method, target, version = startline.split(" ")
        self.parsed_req = Request(method=Method(method), target=target, version=version, headers=headers, body=body)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
