# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

try:
    from io import StringIO
except ImportError:  # Python < 3
    from StringIO import StringIO

from wifi.utils import (print_table, match, db2dbm, set_properties,
get_properties, get_property, ensure_file_exists, MyStringIO)
from mock import patch, MagicMock


print_table_in = [
    ['1', '123456789', 'hello'],
    ['2344566', 'góodbŷe', 'foo']
]
print_table_out = """
1        123456789  hello
2344566  góodbŷe    foo
""".lstrip()


class PrintTableTest(TestCase):
    def test_lengths_formatted_correctly(self):
        stdout = StringIO()
        print_table(print_table_in, file=stdout)
        self.assertEqual(stdout.getvalue(), print_table_out)

    def test_no_failure_with_non_strs(self):
        stdout = StringIO()
        print_table([[1], ['2']], file=stdout)
        self.assertEqual(stdout.getvalue(), '1\n2\n')


class FuzzyMatchTest(TestCase):
    def test_match(self):
        assert match('f', 'foo') > 0
        assert match('x', 'foo') == 0
        assert match('hl', 'hello') > 0
        assert match('hel', 'hello') > match('ho', 'hello')


class db2dbMTest(TestCase):
    def test_db2dbm(self):
        self.assertEqual(db2dbm(-10), -100)
        self.assertEqual(db2dbm(0), -100)
        self.assertEqual(db2dbm(1), -99)
        self.assertEqual(db2dbm(2), -99)
        self.assertEqual(db2dbm(50), -75)
        self.assertEqual(db2dbm(99), -50)
        self.assertEqual(db2dbm(100), -50)
        self.assertEqual(db2dbm(101), -50)
        self.assertEqual(db2dbm(200), -50)


properties_file_content = """scheme_current=test-scheme
interface_current=test-interface
scheme_active=True
"""
properties_file = MyStringIO(properties_file_content)

class propertiesTest(TestCase):
    def test_get_properties(self):
        with patch('__builtin__.open', return_value=properties_file):
            properties = get_properties()
            self.assertEqual(properties['scheme_current'], 'test-scheme')
            self.assertEqual(properties['interface_current'], 'test-interface')
            self.assertEqual(properties['scheme_active'], 'True')
        
    def test_set_properties(self):
        with patch('__builtin__.open', return_value=properties_file):
            properties_to_set = {'scheme_current' : 'test-scheme00',
            'scheme_active' : 'False',
            'interface_current' : 'test-interface00'}
            set_properties(**properties_to_set)
            properties = get_properties()
            self.assertEqual(properties['scheme_current'], 'test-scheme00')
            self.assertEqual(properties['interface_current'], 'test-interface00')
            self.assertEqual(properties['scheme_active'], 'False')
            properties_to_set = {'interface_current' : 'test-interface00',
            'scheme_active' : 'True'}
            set_properties(properties_to_set)
            properties = get_properties()
            self.assertEqual(properties['scheme_current'], 'test-scheme00')
            self.assertEqual(properties['interface_current'], 'test-interface00')
            self.assertEqual(properties['scheme_active'], 'False')
            properties_to_set = {'scheme_current' : 'test-scheme00',
            'scheme_active' : 'True'}
            set_properties(**properties_to_set)
            properties = get_properties()
            self.assertEqual(properties['scheme_current'], 'test-scheme00')
            self.assertEqual(properties['interface_current'], 'test-interface00')
            self.assertEqual(properties['scheme_active'], 'False')

