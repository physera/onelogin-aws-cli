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

        self._period = period
        self._api = api

        self._running = True
        self._sleep = Event()

    def run(self):
        """
        Create a runtime for the foreground credentials renewal
        """
        while self._running:
            self._api.save_credentials()
            self._sleep.wait(self._period)

    def interrupt(self, signal_num: int, *args):
        """
        Received a shutdown signal.
        Could implement HUP to perform a SAML refresh or something though.
        :param signal_num:
        :param args:
        """

        self._sleep.set()

        print("Shutting down Credentials refresh process...")

        self._running = False

        while self.is_alive():
            self._sleep.wait(1)

        print("Shutdown finished.")
