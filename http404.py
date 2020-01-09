# http objects
import shutil


class Request(object):
    def __init__(self, path, method="GET", headers={}, body=None,
                 protocol="HTTP/1.1"):
        self.path = path
        self.method = method
        self.protocol = protocol
        self.headers = headers
        self.body = body

    @classmethod
    def read_from(cls, stream):
        """reads a request object from a stream"""
        method, path, protocol = stream.readline().split()

        headers = {}
        for line in stream:
            sline = line.strip()
            if len(sline) == 0:
                break
            key, val = sline.split(":", 1)
            headers[key.strip()] = val.strip()

        return cls(path, method, headers, stream, protocol)

class Response(object):
    def __init__(self, status=(200, "OK"), headers={}, body=None,
                 protocol="HTTP/1.1"):
        self.statusn, self.statusval = status
        self.headers = headers
        self.body = body
        self.protocol = protocol

    def write_to(self, stream):
        """
        writes a response object to a stream.
        if self.body is a stream, it will be copied to stream, and
        then closed.
        """
        stream.write("{} {} {}\r\n".format(self.protocol, self.statusn,
                                           self.statusval))

        for key, val in self.headers.items():
            stream.write("{}: {}\r\n".format(key, val))

        stream.write("\r\n")

        if type(self.body) is str or type(self.body) is bytes:
            stream.write(self.body)
        else:
            shutil.copyfileobj(self.body, stream)
            self.body.close()
