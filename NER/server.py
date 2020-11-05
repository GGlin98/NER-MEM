import threading
import webbrowser
import http.server
import socketserver
import os
import json
from MEM import MEM

FILE = 'index.html'
PORT = 8088

# web_dir = os.path.join(os.path.dirname(__file__), 'website')
web_dir = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/website'
os.chdir(web_dir)

classifier = MEM()
classifier.load_model('MEM')


class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.get_all('content-length')[0])
        data = self.rfile.read(length)
        data = data.decode('utf-8')
        data = json.loads(data)
        text = data['text']
        clf = data['clf']
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.flush_headers()

        results = classifier.predict_sentence(text, clf)
        json_result = json.dumps(results)
        self.wfile.write(json_result.encode())


def open_browser():
    """Start a browser after waiting for half a second."""

    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))

    thread = threading.Timer(0.5, _open_browser)
    thread.start()


def start_server():
    """Start the server."""
    # server_address = ("0.0.0.0", PORT)
    server_address = ("localhost", PORT)
    with socketserver.TCPServer(server_address, TestHandler) as httpd:
        print("serving at %s:%s" % server_address)
        httpd.serve_forever()


if __name__ == "__main__":
    open_browser()
    start_server()
