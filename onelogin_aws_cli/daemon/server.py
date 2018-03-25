import socket
from socketserver import BaseRequestHandler, TCPServer
from threading import Thread

from onelogin_aws_cli.configuration import Section


class Server(Thread):
    """Start server in thread"""
    HOST = "localhost"

    def __init__(self, config: Section):
        super().__init__()

        self.config = config
        self.server = TCPServer((self.HOST, self.find_free_port()),
                                ServerHandler)

    def run(self):
        """
        Activate the server; this will keep running until you interrupt the
        program with Ctrl-C
        """

        Thread(target=self.server.serve_forever).start()

    def interrupt(self, signal_num: int, *args):
        """
        Shut the server down
        """
        self.server.shutdown()

    @staticmethod
    def find_free_port() -> int:
        """
        Find a free port to listen on
        :return:
        """
        s = socket.socket()
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port


class ServerHandler(BaseRequestHandler):
    """Handle server requests. Currently performs an echo."""

    def handle(self):
        """Write the data we receive to stdout"""

        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        # just send back the same data, but upper-cased
        self.request.sendall(data.upper())
