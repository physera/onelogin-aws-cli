from unittest import TestCase

from onelogin_aws_cli import OneloginAWS


class TestOneloginAWS(TestCase):
    def test_convert_duration(self):
        for test in [{
            'duration': '200',
            'expected': 200,
        }, {
            'duration': '20s',
            'expected': 20,
        }, {
            'duration': '1m',
            'expected': 60,
        }, {
            'duration': '30m',
            'expected': 1800,
        }, {
            'duration': '1h',
            'expected': 3600
        }, {
            'duration': '12h',
            'expected': 43200
        }, {
            'duration': '1d',
            'expected': 86400
        }, {
            'duration': '6d',
            'expected': 518400
        }, {
            'duration': '1w',
            'expected': 604800
        }]:
            actual = OneloginAWS.convert_duration(test['duration'])
            assert actual == test['expected']
