# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
"""Validator tests"""

import pytest

from configobj import ConfigObj
from configobj.validate import *


class TestBasic(object):
    def test_values_too_small(self, val):
        config = '''
        test1=40
        test2=hello
        test3=3
        test4=5.0
        [section]
            test1=40
            test2=hello
            test3=3
            test4=5.0
            [[sub section]]
                test1=40
                test2=hello
                test3=3
                test4=5.0
        '''.splitlines()
        configspec = '''
        test1= integer(30,50)
        test2= string
        test3=integer
        test4=float(6.0)
        [section ]
            test1=integer(30,50)
            test2=string
            test3=integer
            test4=float(6.0)
            [[sub section]]
                test1=integer(30,50)
                test2=string
                test3=integer
                test4=float(6.0)
        '''.splitlines()
        c1 = ConfigObj(config, configspec=configspec)
        test = c1.validate(val)
        assert test == {
                'test1': True,
                'test2': True,
                'test3': True,
                'test4': False,
                'section': {
                    'test1': True,
                    'test2': True,
                    'test3': True,
                    'test4': False,
                    'sub section': {
                        'test1': True,
                        'test2': True,
                        'test3': True,
                        'test4': False,
                    },
                },
            }

        with pytest.raises(VdtValueTooSmallError) as excinfo:
            val.check(c1.configspec['test4'], c1['test4'])
        assert str(excinfo.value) == 'the value "5.0" is too small.'

    def test_values(self, val):
        val_test_config = '''
            key = 0
            key2 = 1.1
            [section]
            key = some text
            key2 = 1.1, 3.0, 17, 6.8
                [[sub-section]]
                key = option1
                key2 = True'''.splitlines()
        val_test_configspec = '''
            key = integer
            key2 = float
            [section]
            key = string
            key2 = float_list(4)
               [[sub-section]]
               key = option(option1, option2)
               key2 = boolean'''.splitlines()
        val_test = ConfigObj(val_test_config, configspec=val_test_configspec)
        assert val_test.validate(val)
        val_test['key'] = 'text not a digit'
        val_res = val_test.validate(val)
        assert val_res == {'key2': True, 'section': True, 'key': False}

    def test_defaults(self, val):
        configspec = '''
            test1=integer(30,50, default=40)
            test2=string(default="hello")
            test3=integer(default=3)
            test4=float(6.0, default=6.0)
            [section ]
                test1=integer(30,50, default=40)
                test2=string(default="hello")
                test3=integer(default=3)
                test4=float(6.0, default=6.0)
                [[sub section]]
                    test1=integer(30,50, default=40)
                    test2=string(default="hello")
                    test3=integer(default=3)
                    test4=float(6.0, default=6.0)
            '''.splitlines()
        default_test = ConfigObj(['test1=30'], configspec=configspec)
        assert repr(default_test) == "ConfigObj({'test1': '30'})"
        assert default_test.defaults == []
        assert default_test.default_values == {}
        assert default_test.validate(val)
        assert default_test == {
            'test1': 30,
            'test2': 'hello',
            'test3': 3,
            'test4': 6.0,
            'section': {
                'test1': 40,
                'test2': 'hello',
                'test3': 3,
                'test4': 6.0,
                'sub section': {
                    'test1': 40,
                    'test3': 3,
                    'test2': 'hello',
                    'test4': 6.0,
                },
            },
        }

        assert default_test.defaults == ['test2', 'test3', 'test4']
        assert default_test.default_values == {
            'test1': 40, 'test2': 'hello',
            'test3': 3, 'test4': 6.0
        }
        assert default_test.restore_default('test1') == 40
        assert default_test['test1'] == 40
        assert 'test1' in default_test.defaults  # pylint: disable=unsupported-membership-test

        def change(section, key):
            section[key] = 3
        default_test.walk(change)
        assert default_test['section']['sub section']['test4'] == 3

        default_test.restore_defaults()
        assert default_test == {
            'test1': 40,
            'test2': "hello",
            'test3': 3,
            'test4': 6.0,
            'section': {
                'test1': 40,
                'test2': "hello",
                'test3': 3,
                'test4': 6.0,
                'sub section': {
                    'test1': 40,
                    'test2': "hello",
                    'test3': 3,
                    'test4': 6.0
        }}}


class TestStringChecks(object):

    def test_required_string_cannot_be_none(self, val):  # issue #93
        val.check('string(min=1)', None)
        with pytest.raises(VdtMissingValue):
            val.check('string(min=1)', None, missing=True)

    @pytest.mark.parametrize('text', ("text = ", ""))
    def test_required_string_cannot_be_empty_or_missing(self, val, text):  # issue #93
        config = [text]
        configspec = ["text = string(min=1)"]
        configobj = ConfigObj(config, configspec=configspec)
        assert configobj.validate(val, preserve_errors=True) is not True, "Validation should've failed"


class TestListChecks(object):

    TYPESPECS = (
        "'integer', 'string', 'boolean', 'float'",
        "'int', 'str', 'bool', 'float'",
        "int, str, bool, float",
    )

    def test_force_list(self, val):
        config = '''
            scalar = 1
            '''.splitlines()
        configspec = '''
            scalar = force_list
            '''.splitlines()
        configobj = ConfigObj(config, configspec=configspec)
        assert configobj.validate(val, preserve_errors=True) is True, "Validation failed unexpectedly"
        assert configobj['scalar'] == ['1']

    @pytest.mark.parametrize('typespec', TYPESPECS)
    def test_mixed_list(self, val, typespec):
        config = '''
            mixed = 1, 2, yes, 3.1415
            '''.splitlines()
        configspec = '''
            mixed = mixed_list({0})
            '''.format(typespec).splitlines()
        configobj = ConfigObj(config, configspec=configspec)
        assert configobj.validate(val, preserve_errors=True) is True, "Validation failed unexpectedly"
        assert configobj['mixed'] == [1, '2', True, 3.1415]


class TestDottedQuadToNum(object):

    def test_stripped(self):
        assert dottedQuadToNum('192.0.2.0') == 3221225984
        assert dottedQuadToNum('192.0.2.1 ') == 3221225985
        assert dottedQuadToNum(' 192.0.2.2') == 3221225986
        assert dottedQuadToNum('\t\t192.0.2.3\n') == 3221225987
        with pytest.raises(ValueError) as excinfo:
            dottedQuadToNum('192. 0. 2. 4')
        assert str(excinfo.value) == 'Not a good dotted-quad IP: 192. 0. 2. 4'

    def test_boundaries(self):
        assert dottedQuadToNum('0.0.0.0') == 0
        assert dottedQuadToNum('255.255.255.255') == 4294967295
        with pytest.raises(ValueError) as excinfo:
            dottedQuadToNum('255.255.255.256')
        assert str(excinfo.value) == (
            'Not a good dotted-quad IP: 255.255.255.256')
        with pytest.raises(ValueError) as excinfo:
            dottedQuadToNum('-1')
        assert str(excinfo.value) == 'Not a good dotted-quad IP: -1'
