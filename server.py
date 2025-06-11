from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.error
from urllib.parse import urlparse
import os

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL
        url = urlparse(self.path)
        
        # If the path starts with /api, proxy to Flask backend
        if url.path.startswith('/api/'):
            backend_url = f'http://localhost:5000{url.path}'
            try:
                # Forward the request to the backend
                with urllib.request.urlopen(backend_url) as response:
                    # Copy status code
                    self.send_response(response.status)
                    
                    # Copy headers
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    # Copy content
                    self.wfile.write(response.read())
            except urllib.error.URLError as e:
                self.send_error(500, f"Backend error: {str(e)}")
            return

        # For all other paths, serve static files from frontend/public
        self.path = f'/frontend/public{url.path}'
        if self.path == '/frontend/public/':
            self.path = '/frontend/public/index.html'
        
        try:
            return SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            self.send_error(404, f"File not found")

if __name__ == '__main__':
    os.chdir('/project/sandbox/user-workspace')  # Set working directory
    server = HTTPServer(('', 8000), ProxyHandler)
    print('Starting server on port 8000...')
    server.serve_forever()
