import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query_params)
        
        verify_token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")
        
        if verify_token and challenge and verify_token[0] == os.environ.get("VERIFY_TOKEN"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(challenge[0].encode("utf-8"))
        else:
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    server_address = ('', int(os.environ.get("PORT", 8080)))
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
