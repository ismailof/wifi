from __future__ import print_function, unicode_literals, division

import os
import sys


if sys.version < '3':
    str = unicode

try:
    from io import StringIO
except ImportError:  # Python < 3
    from StringIO import StringIO

def match(needle, haystack):
    """
    Command-T-style string matching.
    """
    score = 1
    j = 0
    last_match = 0
    needle = needle.lower()
    haystack = haystack.lower()

    for c in needle:
        while j < len(haystack) and haystack[j] != c:
            j += 1
        if j >= len(haystack):
            return 0
        score += 1 / (last_match + 1.)
        last_match = j
        j += 1
    return score


def print_table(matrix, sep='  ', file=sys.stdout, *args, **kwargs):
    """
    Prints a left-aligned table of elements.
    """
    lengths = [max(map(len, map(str, column))) for column in zip(*matrix)]
    format = sep.join('{{{0}:<{1}}}'.format(i, length) for i, length in enumerate(lengths))

    for row in matrix:
        print(format.format(*row).strip(), file=file, *args, **kwargs)


def db2dbm(quality):
    """
    Converts the Radio (Received) Signal Strength Indicator (in db) to a dBm
    value.  Please see http://stackoverflow.com/a/15798024/1013960
    """
    dbm = int((quality / 2) - 100)
    return min(max(dbm, -100), -50)


def ensure_file_exists(filename):
    """
    http://stackoverflow.com/a/12654798/1013960
    """
    if not os.path.exists(filename):
        open(filename, 'a').close()

rconf_file = '.runningconfig'
#runnig config file
ensure_file_exists(rconf_file)

def set_properties(interface_current=None, scheme_current=None, scheme_active=False):
    properties = get_properties()
    if not (bool(interface_current) ^ bool(scheme_current)):
        properties['scheme_active'] = scheme_active
        if interface_current and scheme_active:
            properties['interface_current'] = interface_current
            properties['scheme_current'] = scheme_current
        f = open(rconf_file, 'w')
        for prop in properties:
            prop_line = str(prop) + '=' + str(properties[prop]) + '\n'
            f.write(prop_line)
        f.close()

def get_properties():
    f = open(rconf_file, 'r')
    properties = dict()
    for line in f:
        prop, prop_value = line.replace('\n', '').split('=')
        properties[prop] = prop_value
    f.close()
    return properties

def get_property(prop):
    properties = get_properties()
    return properties[prop]

class MyStringIO(StringIO):
# extends StringIO buit-in class to override write and close methods
# for testing IO operations.

    def __init__(self, string):
        super(MyStringIO, self).__init__(string)
        self.truncate = False
    
    def write(self, string):
        if self.truncate:
            self.__init__(string)
        else:
            value = self.getvalue() + string
            self.__init__(value)
    
    def close(self):
        self.truncate = True
        self.seek(0)
