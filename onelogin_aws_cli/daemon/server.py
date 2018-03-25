import socketserver
from threading import Thread


class Server(Thread):

    def __init__(self, config):
        self.config = config

    def run(self):
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), Server) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
