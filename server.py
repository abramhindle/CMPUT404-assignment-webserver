#  coding: utf-8
import dataclasses
import enum
import socketserver
import sys
import urllib.parse

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Mattwmaster58
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
from pathlib import Path
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

print(f"\n(__file__)={__file__}")

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
            b"\r\n",
            b"" if self.body is None else self.body
        ])


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.set_parsed_req()
        print(f"request: {self.parsed_req}")
        self.set_resp()
        print(f"response formulated: {self.resp}")
        self.request.sendall(self.resp.serialize())

    def set_resp(self):
        if self.parsed_req.method != Method.GET:
            self.resp = Response(405)
            return

        # www = Path(__file__).parent / "www"
        www = Path(__file__).absolute().parent / "www"
        resource_path = (www / f".{self.parsed_req.target}").resolve()
        if resource_path.is_dir():
            if not self.parsed_req.target.endswith("/"):
                self.resp = Response(301, {"Location": self.parsed_req.target + "/"})
                return

            resource_path = resource_path / "index.html"
        # not found + hacky way to resist path traversal attack
        if not resource_path.exists() or not resource_path.as_posix().startswith(www.as_posix()):
            self.resp = Response(404)
        else:
            suffix = resource_path.suffix.strip(".").lower()
            mime_type = f"text/{suffix}"
            body = resource_path.read_bytes()
            self.resp = Response(200, {"Content-Type": f"{mime_type}; charset=utf-8"}, body)

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
        target = urllib.parse.unquote(target)
        self.parsed_req = Request(method=Method(method), target=target, version=version, headers=headers, body=body)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
