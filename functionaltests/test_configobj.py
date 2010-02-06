from __future__ import with_statement

import os
import unittest
from configobj import ConfigObj

from warnings import catch_warnings


class TestConfigObj(unittest.TestCase):
    
    def test_order_preserved(self):
        c = ConfigObj()
        c['a'] = 1
        c['b'] = 2
        c['c'] = 3
        c['section'] = {}
        c['section']['a'] = 1
        c['section']['b'] = 2
        c['section']['c'] = 3
        c['section']['section'] = {}
        c['section']['section2'] = {}
        c['section']['section3'] = {}
        c['section2'] = {}
        c['section3'] = {}
        
        c2 = ConfigObj(c)
        self.assertEqual(c2.scalars, ['a', 'b', 'c'])
        self.assertEqual(c2.sections, ['section', 'section2', 'section3'])
        self.assertEqual(c2['section'].scalars, ['a', 'b', 'c'])
        self.assertEqual(c2['section'].sections, ['section', 'section2', 'section3'])
        
        self.assertFalse(c['section'] is c2['section'])
        self.assertFalse(c['section']['section'] is c2['section']['section'])
    
    def test_options_deprecation(self):
        with catch_warnings(record=True) as log:
            ConfigObj(options={})
        
        # unpack the only member of log
        warning, = log
        self.assertEqual(warning.category, DeprecationWarning)