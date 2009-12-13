import os
import unittest
from configobj import ConfigObj

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
        self.assertEqual(c2['section'].c.sections, ['section', 'section2', 'section3'])