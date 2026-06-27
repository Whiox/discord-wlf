
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import registry


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/health": self.handle_health,
            "/metrics": self.handle_metrics,
        }

        path = urlparse(self.path).path
        handler = routes.get(path)
        if handler is None:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return

        handler()

    def handle_health(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok")

    def handle_metrics(self):
        payload = generate_latest(registry)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return


def start_http_server(port: int):
    server = ThreadingHTTPServer(("0.0.0.0", port), RequestHandler)
    server.serve_forever()
