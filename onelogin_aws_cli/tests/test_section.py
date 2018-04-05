from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock

from onelogin_aws_cli import Section


class TestSection(TestCase):
    def test_set_overrides(self):
        sec = Section('mock-section', Namespace(
            get=MagicMock(return_value='world')
        ))

        self.assertEqual(sec['foo'], 'world')

        sec.set_overrides(dict(
            foo='bar'
        ))

        self.assertEqual(sec['foo'], 'bar')
