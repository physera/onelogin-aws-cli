import socketserver
from threading import Thread

from onelogin_aws_cli.configuration import Section


class Server(Thread):
    """Start server in thread"""
    HOST = "localhost"
    PORT = 9999

    def __init__(self, config: Section):
        super().__init__()
        self.config = config

    def run(self):
        """Start our server on specificed port"""

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((self.HOST, self.PORT),
                                    ServerHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()


class ServerHandler(socketserver.BaseRequestHandler):
    """Handle server requests. Currently performs an echo."""

    def handle(self):
        """Write the data we receive to stdout"""

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
