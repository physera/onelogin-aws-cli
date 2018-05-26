from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock

from onelogin_aws_cli import Section


class TestSection(TestCase):

    def test___contains__true(self):
        sec = Section('mock-section', Namespace(
            has_option=MagicMock(return_value=True),
            getboolean=lambda item: item,
        ))
        self.assertTrue('mock' in sec)

    def test___contains__false(self):
        sec = Section('mock-section', Namespace(
            has_option=MagicMock(return_value=False),
            DEFAULTS=dict(),
            getboolean=lambda item: item,
        ))
        self.assertFalse('mock' in sec)

    def test_set_overrides(self):
        sec = Section('mock-section', MagicMock(
            get=MagicMock(return_value='world'),
            has_option=MagicMock(return_value=True)
        ))

        self.assertEqual(sec['foo'], 'world')

        sec.set_overrides(dict(
            foo='bar'
        ))

        self.assertEqual(sec['foo'], 'bar')

    def test_has_required_false(self):
        sec = Section('mock-section', MagicMock(
            has_option=MagicMock(side_effect=lambda s, x: x != 'base_uri')
        ))

        self.assertFalse(sec.get('has_required'))

    def test_has_required_true(self):
        sec = Section('mock-section', MagicMock(
            has_option=MagicMock(return_value=True)
        ))

        self.assertTrue(sec.get('has_required'))

    def test__has_cast_handler(self):
        sec = Section('mock-section', MagicMock(
            getboolean=lambda item: item,
        ))

        self.assertTrue(sec._has_cast_handler('can_mock'))

        self.assertFalse(sec._has_cast_handler('cannot_mock'))
        self.assertFalse(sec._has_cast_handler('wont_mock'))
