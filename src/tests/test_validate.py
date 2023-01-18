# coding=utf-8

from configobj import ConfigObj
import pytest
from configobj.validate import Validator, VdtValueTooSmallError


class TestImporting(object):
    def test_top_level(self, val):
        import validate
        assert val.__class__ is validate.Validator

    def test_within_configobj_using_from(self, val):
        from configobj import validate
        assert val.__class__ is validate.Validator

    def test_within_configobj(self, val):
        import configobj.validate
        assert val.__class__ is configobj.validate.Validator


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
        assert 'test1' in default_test.defaults

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
