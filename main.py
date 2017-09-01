#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import httplib
import zlib
import sys

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = httplib.HTTPSConnection(REMOTE_SERVER)
        request_headers = dict()
        for header in self.headers:
            print header, ':', self.headers[header]
            value = self.headers[header]
            if header == "host":
                value = REMOTE_SERVER
            request_headers[header] = value

        if self.command == "GET":
            conn.request(self.command, self.path, headers=request_headers)
        else:
            request_body = self.rfile.read(int(self.headers.getheader('content-length')))
            print request_body
            conn.request(self.command, self.path, request_body, request_headers)
        res = conn.getresponse()

        self.send_response(res.status)
        for header in res.getheaders():
            print header
            self.send_header(header[0], header[1])
        self.end_headers()
        response_body = res.read()
        decompressed_body = response_body
        if res.getheader('content-encoding') == 'gzip':
            decompressed_body = zlib.decompress(response_body, 31)
        print decompressed_body
        self.wfile.write(response_body)
        conn.close()

    def do_POST(self):
        self.do_GET()


REMOTE_SERVER = sys.argv[1]
SERVER_ADDRESS = ('', 28021)
HTTPD = HTTPServer(SERVER_ADDRESS, RequestHandler)
HTTPD.serve_forever()


