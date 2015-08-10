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
#from wifi import subprocess_compat as subprocess
from wifi.scheme import Scheme


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

connected_output = """test-interface00     IEEE 802.11bgn  ESSID:"test-essid"  
          Mode:Managed  Frequency:2.412 GHz  Access Point: 70:62:B8:52:7A:00   
          Bit Rate=72.2 Mb/s   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr=2347 B   Fragment thr:off
          Power Management:off
          Link Quality=50/70  Signal level=-60 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:8   Missed beacon:0
"""

disconnected_output = """test-interface00     IEEE 802.11bgn  ESSID:off/any  
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr=2347 B   Fragment thr:off
          Power Management:off
"""

config = {'wireless-essid' : 'test-essid',}
test_scheme00 = Scheme('test-interface00', 'test-scheme00')
test_scheme = Scheme('test-interface', 'test-scheme')

#def return_scheme(interface_current, scheme_current):
#    return Scheme(interface_current, scheme_current, options=config)

class propertiesTest(TestCase):
    def test_get_properties(self):
        with patch('__builtin__.open', return_value=properties_file):
            properties = get_properties()
            self.assertEqual(properties['scheme_current'], 'test-scheme')
            self.assertEqual(properties['interface_current'], 'test-interface')
            self.assertEqual(properties['scheme_active'], 'True')
        
    def test_set_properties(self):
        with patch('wifi.scheme.Scheme.find', return_value=test_scheme00):
            # when disconnected
            with patch('__builtin__.open', return_value=properties_file):
                with patch('wifi.subprocess_compat.check_output',
                return_value=disconnected_output):
                    properties_to_set = {
                    'scheme_current' : 'test-scheme00',
                    'interface_current' : 'test-interface00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'False')
                    properties_to_set = {
                    'interface_current' : 'test-interface00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'False')
                    properties_to_set = {
                    'scheme_current' : 'test-scheme00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'False')
            # when actually connected
            with patch('__builtin__.open', return_value=properties_file):
                with patch('wifi.subprocess_compat.check_output',
                return_value=connected_output):
                    properties_to_set = {
                    'scheme_current' : 'test-scheme00',
                    'interface_current' : 'test-interface00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'True')
                    properties_to_set = {
                    'interface_current' : 'test-interface00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'True')
                    properties_to_set = {
                    'scheme_current' : 'test-scheme00'}
                    set_properties(config=config, **properties_to_set)
                    properties = get_properties()
                    self.assertEqual(properties['scheme_current'],
                    'test-scheme00')
                    self.assertEqual(properties['interface_current'],
                    'test-interface00')
                    self.assertEqual(properties['scheme_active'], 'True')
                # trying to activate current scheme
                with patch('wifi.utils.get_properties',
                return_value=properties):
                    with patch('wifi.subprocess_compat.check_output',
                    return_value=connected_output):
                        set_properties(config=config)
                        self.assertEqual(properties['scheme_active'],
                        'True')
                    with patch('wifi.subprocess_compat.check_output',
                    return_value=disconnected_output):
                        set_properties(config=config)
                        self.assertEqual(properties['scheme_active'],
                        'False')

