"""
Provide the foreground Process as a Thread
"""
from threading import Event, Thread

from onelogin_aws_cli import OneloginAWS


class ForegroundProcess(Thread):
    """
    Run the credentials renewal process in a process
    """

    def __init__(self, period: int, api: OneloginAWS):
        super().__init__()

        self.period = period
        self.api = api

        self.running = True
        self.sleep = Event()

    def run(self):
        """
        Create a runtime for the foreground credentials renewal
        """
        while self.running:
            self.api.save_credentials()
            self.sleep.wait(self.period)

    def interrupt(self, signal_num: int, *args):
        """
        Received a shutdown signal.
        Could implement HUP to perform a SAML refresh or something though.
        :param signal_num:
        :param args:
        """

        print("Shutting down Credentials refresh process...")

        self.running = False
        self.sleep.set()

        print("Shutdown finished.")
