from threading import Event
from unittest import TestCase

from onelogin_aws_cli.daemon.foreground import ForegroundProcess


class MockApi(object):
    def save_credentials(self):
        Event().wait(1)


class TestForegroundProcess(TestCase):
    def setUp(self):
        self.api = MockApi()

    def test_run(self):
        process = ForegroundProcess(period=1, api=self.api)
        self.assertEqual(process._period, 1)
        self.assertEqual(process._api, self.api)
        self.assertEqual(process._running, False)
        self.assertIsInstance(process._sleep, Event)

    def test_interrupt(self):
        process = ForegroundProcess(period=1, api=self.api)
