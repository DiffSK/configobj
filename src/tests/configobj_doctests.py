# configobj_test.py
# doctests for ConfigObj
# A config file reader/writer that supports nested sections in config files.
# Copyright (C) 2005-2014:
# (name) : (email)
# Michael Foord: fuzzyman AT voidspace DOT org DOT uk
# Nicola Larosa: nico AT tekNico DOT net
# Rob Dennis: rdennis AT gmail DOT com
# Eli Courtwright: eli AT courtwright DOT org

# This software is licensed under the terms of the BSD license.
# http://opensource.org/licenses/BSD-3-Clause

# ConfigObj 5 - main repository for documentation and issue tracking:
# https://github.com/DiffSK/configobj

import sys

from io import StringIO

import sys

from configobj import *
from configobj.validate import Validator


def _test_validate():
    """
    >>> val = Validator()

    >>> a = ['foo = fish']
    >>> b = ['foo = integer(default=3)']
    >>> c = ConfigObj(a, configspec=b)
    >>> c
    ConfigObj({'foo': 'fish'})
    >>> from configobj.validate import Validator
    >>> v = Validator()
    >>> c.validate(v)
    0
    >>> c.default_values
    {'foo': 3}
    >>> c.restore_default('foo')
    3

    Now testing with repeated sections : BIG TEST
    
    >>> repeated_1 = '''
    ... [dogs]
    ...     [[__many__]] # spec for a dog
    ...         fleas = boolean(default=True)
    ...         tail = option(long, short, default=long)
    ...         name = string(default=rover)
    ...         [[[__many__]]]  # spec for a puppy
    ...             name = string(default="son of rover")
    ...             age = float(default=0.0)
    ... [cats]
    ...     [[__many__]] # spec for a cat
    ...         fleas = boolean(default=True)
    ...         tail = option(long, short, default=short)
    ...         name = string(default=pussy)
    ...         [[[__many__]]] # spec for a kitten
    ...             name = string(default="son of pussy")
    ...             age = float(default=0.0)
    ...         '''.split('\\n')
    >>> repeated_2 = '''
    ... [dogs]
    ... 
    ...     # blank dogs with puppies
    ...     # should be filled in by the configspec
    ...     [[dog1]]
    ...         [[[puppy1]]]
    ...         [[[puppy2]]]
    ...         [[[puppy3]]]
    ...     [[dog2]]
    ...         [[[puppy1]]]
    ...         [[[puppy2]]]
    ...         [[[puppy3]]]
    ...     [[dog3]]
    ...         [[[puppy1]]]
    ...         [[[puppy2]]]
    ...         [[[puppy3]]]
    ... [cats]
    ... 
    ...     # blank cats with kittens
    ...     # should be filled in by the configspec
    ...     [[cat1]]
    ...         [[[kitten1]]]
    ...         [[[kitten2]]]
    ...         [[[kitten3]]]
    ...     [[cat2]]
    ...         [[[kitten1]]]
    ...         [[[kitten2]]]
    ...         [[[kitten3]]]
    ...     [[cat3]]
    ...         [[[kitten1]]]
    ...         [[[kitten2]]]
    ...         [[[kitten3]]]
    ... '''.split('\\n')
    >>> repeated_3 = '''
    ... [dogs]
    ... 
    ...     [[dog1]]
    ...     [[dog2]]
    ...     [[dog3]]
    ... [cats]
    ... 
    ...     [[cat1]]
    ...     [[cat2]]
    ...     [[cat3]]
    ... '''.split('\\n')
    >>> repeated_4 = '''
    ... [__many__]
    ... 
    ...     name = string(default=Michael)
    ...     age = float(default=0.0)
    ...     sex = option(m, f, default=m)
    ... '''.split('\\n')
    >>> repeated_5 = '''
    ... [cats]
    ... [[__many__]]
    ...     fleas = boolean(default=True)
    ...     tail = option(long, short, default=short)
    ...     name = string(default=pussy)
    ...     [[[description]]]
    ...         height = float(default=3.3)
    ...         weight = float(default=6)
    ...         [[[[coat]]]]
    ...             fur = option(black, grey, brown, "tortoise shell", default=black)
    ...             condition = integer(0,10, default=5)
    ... '''.split('\\n')
    >>> val= Validator()
    >>> repeater = ConfigObj(repeated_2, configspec=repeated_1)
    >>> repeater.validate(val)
    1
    >>> repeater == {
    ...     'dogs': {
    ...         'dog1': {
    ...             'fleas': True,
    ...             'tail': 'long',
    ...             'name': 'rover',
    ...             'puppy1': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy2': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy3': {'name': 'son of rover', 'age': 0.0},
    ...         },
    ...         'dog2': {
    ...             'fleas': True,
    ...             'tail': 'long',
    ...             'name': 'rover',
    ...             'puppy1': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy2': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy3': {'name': 'son of rover', 'age': 0.0},
    ...         },
    ...         'dog3': {
    ...             'fleas': True,
    ...             'tail': 'long',
    ...             'name': 'rover',
    ...             'puppy1': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy2': {'name': 'son of rover', 'age': 0.0},
    ...             'puppy3': {'name': 'son of rover', 'age': 0.0},
    ...         },
    ...     },
    ...     'cats': {
    ...         'cat1': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'kitten1': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten2': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten3': {'name': 'son of pussy', 'age': 0.0},
    ...         },
    ...         'cat2': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'kitten1': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten2': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten3': {'name': 'son of pussy', 'age': 0.0},
    ...         },
    ...         'cat3': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'kitten1': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten2': {'name': 'son of pussy', 'age': 0.0},
    ...             'kitten3': {'name': 'son of pussy', 'age': 0.0},
    ...         },
    ...     },
    ... }
    1
    >>> repeater = ConfigObj(repeated_3, configspec=repeated_1)
    >>> repeater.validate(val)
    1
    >>> repeater == {
    ...     'cats': {
    ...         'cat1': {'fleas': True, 'tail': 'short', 'name': 'pussy'},
    ...         'cat2': {'fleas': True, 'tail': 'short', 'name': 'pussy'},
    ...         'cat3': {'fleas': True, 'tail': 'short', 'name': 'pussy'},
    ...     },
    ...     'dogs': {
    ...         'dog1': {'fleas': True, 'tail': 'long', 'name': 'rover'},
    ...         'dog2': {'fleas': True, 'tail': 'long', 'name': 'rover'},
    ...         'dog3': {'fleas': True, 'tail': 'long', 'name': 'rover'},
    ...     },
    ... }
    1
    >>> repeater = ConfigObj(configspec=repeated_4)
    >>> repeater['Michael'] = {}
    >>> repeater.validate(val)
    1
    >>> repeater == {
    ...     'Michael': {'age': 0.0, 'name': 'Michael', 'sex': 'm'},
    ... }
    1
    >>> repeater = ConfigObj(repeated_3, configspec=repeated_5)
    >>> repeater == {
    ...     'dogs': {'dog1': {}, 'dog2': {}, 'dog3': {}},
    ...     'cats': {'cat1': {}, 'cat2': {}, 'cat3': {}},
    ... }
    1
    >>> repeater.validate(val)
    1
    >>> repeater == {
    ...     'dogs': {'dog1': {}, 'dog2': {}, 'dog3': {}},
    ...     'cats': {
    ...         'cat1': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'description': {
    ...                 'weight': 6.0,
    ...                 'height': 3.2999999999999998,
    ...                 'coat': {'fur': 'black', 'condition': 5},
    ...             },
    ...         },
    ...         'cat2': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'description': {
    ...                 'weight': 6.0,
    ...                 'height': 3.2999999999999998,
    ...                 'coat': {'fur': 'black', 'condition': 5},
    ...             },
    ...         },
    ...         'cat3': {
    ...             'fleas': True,
    ...             'tail': 'short',
    ...             'name': 'pussy',
    ...             'description': {
    ...                 'weight': 6.0,
    ...                 'height': 3.2999999999999998,
    ...                 'coat': {'fur': 'black', 'condition': 5},
    ...             },
    ...         },
    ...     },
    ... }
    1
    
    Test that interpolation is preserved for validated string values.
    Also check that interpolation works in configspecs.
    >>> t = ConfigObj(configspec=['test = string'])
    >>> t['DEFAULT'] = {}
    >>> t['DEFAULT']['def_test'] = 'a'
    >>> t['test'] = '%(def_test)s'
    >>> t['test']
    'a'
    >>> v = Validator()
    >>> t.validate(v)
    1
    >>> t.interpolation = False
    >>> t
    ConfigObj({'test': '%(def_test)s', 'DEFAULT': {'def_test': 'a'}})
    >>> specs = [
    ...    'interpolated string  = string(default="fuzzy-%(man)s")',
    ...    '[DEFAULT]',
    ...    'man = wuzzy',
    ...    ]
    >>> c = ConfigObj(configspec=specs)
    >>> c.validate(v)
    1
    >>> c['interpolated string']
    'fuzzy-wuzzy'

    Test SimpleVal
    >>> val = SimpleVal()
    >>> config = '''
    ... test1=40
    ... test2=hello
    ... test3=3
    ... test4=5.0
    ... [section]
    ... test1=40
    ... test2=hello
    ... test3=3
    ... test4=5.0
    ...     [[sub section]]
    ...     test1=40
    ...     test2=hello
    ...     test3=3
    ...     test4=5.0
    ... '''.split('\\n')
    >>> configspec = '''
    ... test1=''
    ... test2=''
    ... test3=''
    ... test4=''
    ... [section]
    ... test1=''
    ... test2=''
    ... test3=''
    ... test4=''
    ...     [[sub section]]
    ...     test1=''
    ...     test2=''
    ...     test3=''
    ...     test4=''
    ... '''.split('\\n')
    >>> o = ConfigObj(config, configspec=configspec)
    >>> o.validate(val)
    1
    >>> o = ConfigObj(configspec=configspec)
    >>> o.validate(val)
    0
    
    Test Flatten Errors
    >>> vtor = Validator()
    >>> my_ini = '''
    ...     option1 = True
    ...     [section1]
    ...     option1 = True
    ...     [section2]
    ...     another_option = Probably
    ...     [section3]
    ...     another_option = True
    ...     [[section3b]]
    ...     value = 3
    ...     value2 = a
    ...     value3 = 11
    ...     '''
    >>> my_cfg = '''
    ...     option1 = boolean()
    ...     option2 = boolean()
    ...     option3 = boolean(default=Bad_value)
    ...     [section1]
    ...     option1 = boolean()
    ...     option2 = boolean()
    ...     option3 = boolean(default=Bad_value)
    ...     [section2]
    ...     another_option = boolean()
    ...     [section3]
    ...     another_option = boolean()
    ...     [[section3b]]
    ...     value = integer
    ...     value2 = integer
    ...     value3 = integer(0, 10)
    ...         [[[section3b-sub]]]
    ...         value = string
    ...     [section4]
    ...     another_option = boolean()
    ...     '''
    >>> cs = my_cfg.split('\\n')
    >>> ini = my_ini.split('\\n')
    >>> cfg = ConfigObj(ini, configspec=cs)
    >>> res = cfg.validate(vtor, preserve_errors=True)
    >>> errors = []
    >>> for entry in flatten_errors(cfg, res):
    ...     section_list, key, error = entry
    ...     section_list.insert(0, '[root]')
    ...     if key is not None:
    ...         section_list.append(key)
    ...     section_string = ', '.join(section_list)
    ...     errors.append('%s%s%s' % (section_string, ' = ', error or 'missing'))
    >>> errors.sort()
    >>> for entry in errors:
    ...     print(entry)
    [root], option2 = missing
    [root], option3 = the value "Bad_value" is of the wrong type.
    [root], section1, option2 = missing
    [root], section1, option3 = the value "Bad_value" is of the wrong type.
    [root], section2, another_option = the value "Probably" is of the wrong type.
    [root], section3, section3b, section3b-sub = missing
    [root], section3, section3b, value2 = the value "a" is of the wrong type.
    [root], section3, section3b, value3 = the value "11" is too big.
    [root], section4 = missing
    """


def _test_errors():
    """
    Test the error messages and objects, in normal mode and unrepr mode.
    >>> bad_syntax = '''
    ... key = "value"
    ... key2 = "value
    ... '''.splitlines()
    >>> c = ConfigObj(bad_syntax)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 3.
    >>> c = ConfigObj(bad_syntax, raise_errors=True)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 3.
    >>> c = ConfigObj(bad_syntax, raise_errors=True, unrepr=True)
    Traceback (most recent call last):
    UnreprError: Parse error in value at line 3.
    >>> try:
    ...     c = ConfigObj(bad_syntax)
    ... except Exception as exc:
    ...     e = exc
    >>> assert(isinstance(e, ConfigObjError))
    >>> print(e)
    Parse error in value at line 3.
    >>> len(e.errors) == 1
    1
    >>> try:
    ...     c = ConfigObj(bad_syntax, unrepr=True)
    ... except Exception as exc:
    ...     e = exc
    >>> assert(isinstance(e, ConfigObjError))
    >>> print(e)
    Parse error from unrepr-ing value at line 3.
    >>> len(e.errors) == 1
    1
    >>> the_error = e.errors[0]
    >>> assert(isinstance(the_error, UnreprError))
    
    >>> multiple_bad_syntax = '''
    ... key = "value"
    ... key2 = "value
    ... key3 = "value2
    ... '''.splitlines()
    >>> try:
    ...     c = ConfigObj(multiple_bad_syntax)
    ... except ConfigObjError as e:
    ...     str(e)
    'Parsing failed with several errors.\\nFirst error at line 3.'
    >>> c = ConfigObj(multiple_bad_syntax, raise_errors=True)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 3.
    >>> c = ConfigObj(multiple_bad_syntax, raise_errors=True, unrepr=True)
    Traceback (most recent call last):
    UnreprError: Parse error in value at line 3.
    >>> try:
    ...     c = ConfigObj(multiple_bad_syntax)
    ... except Exception as exc:
    ...     e = exc
    >>> assert(isinstance(e, ConfigObjError))
    >>> print(e)
    Parsing failed with several errors.
    First error at line 3.
    >>> len(e.errors) == 2
    1
    >>> try:
    ...     c = ConfigObj(multiple_bad_syntax, unrepr=True)
    ... except Exception as exc:
    ...     e = exc
    >>> assert(isinstance(e, ConfigObjError))
    >>> print(e)
    Parsing failed with several errors.
    First error at line 3.
    >>> len(e.errors) == 2
    1
    >>> the_error = e.errors[1]
    >>> assert(isinstance(the_error, UnreprError))
    
    >>> unknown_name = '''
    ... key = "value"
    ... key2 = value
    ... '''.splitlines()
    >>> c = ConfigObj(unknown_name)
    >>> c = ConfigObj(unknown_name, unrepr=True)
    Traceback (most recent call last):
    UnreprError: Unknown name or type in value at line 3.
    >>> c = ConfigObj(unknown_name, raise_errors=True, unrepr=True)
    Traceback (most recent call last):
    UnreprError: Unknown name or type in value at line 3.
    """


def _test_validate_with_copy_and_many():
    """
    >>> spec = '''
    ... [section]
    ... [[__many__]]
    ... value = string(default='nothing')
    ... '''
    >>> config = '''
    ... [section]
    ... [[something]]
    ... '''
    >>> c = ConfigObj(StringIO(config), configspec=StringIO(spec))
    >>> v = Validator()
    >>> r = c.validate(v, copy=True)
    >>> c['section']['something']['value'] == 'nothing'
    True
    """
    
def _test_configspec_with_hash():
    """
    >>> spec = ['stuff = string(default="#ff00dd")']
    >>> c = ConfigObj(spec, _inspec=True)
    >>> c['stuff']
    'string(default="#ff00dd")'
    >>> c = ConfigObj(configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> c['stuff']
    '#ff00dd'
    
    
    >>> spec = ['stuff = string(default="fish") # wooble']
    >>> c = ConfigObj(spec, _inspec=True)
    >>> c['stuff']
    'string(default="fish") # wooble'
    """

def _test_many_check():
    """
    >>> spec = ['__many__ = integer()']
    >>> config = ['a = 6', 'b = 7']
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['a'], int)
    True
    >>> isinstance(c['b'], int)
    True
    
    
    >>> spec = ['[name]', '__many__ = integer()']
    >>> config = ['[name]', 'a = 6', 'b = 7']
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['name']['a'], int)
    True
    >>> isinstance(c['name']['b'], int)
    True
    
    
    >>> spec = ['[__many__]', '__many__ = integer()']
    >>> config = ['[name]', 'hello = 7', '[thing]', 'fish = 0']
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['name']['hello'], int)
    True
    >>> isinstance(c['thing']['fish'], int)
    True
    
    
    >>> spec = '''
    ... ___many___ = integer
    ... [__many__]
    ... ___many___ = boolean
    ... [[__many__]]
    ... __many__ = float
    ... '''.splitlines()
    >>> config = '''
    ... fish = 8
    ... buggle = 4
    ... [hi]
    ... one = true
    ... two = false
    ... [[bye]]
    ... odd = 3
    ... whoops = 9.0
    ... [bye]
    ... one = true
    ... two = true
    ... [[lots]]
    ... odd = 3
    ... whoops = 9.0
    ... '''.splitlines()
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['fish'], int)
    True
    >>> isinstance(c['buggle'], int)
    True
    >>> c['hi']['one']
    1
    >>> c['hi']['two']
    0
    >>> isinstance(c['hi']['bye']['odd'], float)
    True
    >>> isinstance(c['hi']['bye']['whoops'], float)
    True
    >>> c['bye']['one']
    1
    >>> c['bye']['two']
    1
    >>> isinstance(c['bye']['lots']['odd'], float)
    True
    >>> isinstance(c['bye']['lots']['whoops'], float)
    True
    
    
    >>> spec = ['___many___ = integer()']
    >>> config = ['a = 6', 'b = 7']
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['a'], int)
    True
    >>> isinstance(c['b'], int)
    True

    
    >>> spec = '''
    ... [__many__]
    ... [[__many__]]
    ... __many__ = float
    ... '''.splitlines()
    >>> config = '''
    ... [hi]
    ... [[bye]]
    ... odd = 3
    ... whoops = 9.0
    ... [bye]
    ... [[lots]]
    ... odd = 3
    ... whoops = 9.0
    ... '''.splitlines()
    >>> c = ConfigObj(config, configspec=spec)
    >>> v = Validator()
    >>> c.validate(v)
    1
    >>> isinstance(c['hi']['bye']['odd'], float)
    True
    >>> isinstance(c['hi']['bye']['whoops'], float)
    True
    >>> isinstance(c['bye']['lots']['odd'], float)
    True
    >>> isinstance(c['bye']['lots']['whoops'], float)
    True
    
    >>> s = ['[dog]', '[[cow]]', 'something = boolean', '[[__many__]]', 
    ...      'fish = integer']
    >>> c = ['[dog]', '[[cow]]', 'something = true', '[[ob]]', 
    ...      'fish = 3', '[[bo]]', 'fish = 6']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v)
    1
    >>> ini['dog']['cow']['something']
    1
    >>> ini['dog']['ob']['fish']
    3
    >>> ini['dog']['bo']['fish']
    6
    
    
    >>> s = ['[cow]', 'something = boolean', '[__many__]', 
    ...      'fish = integer']
    >>> c = ['[cow]', 'something = true', '[ob]', 
    ...      'fish = 3', '[bo]', 'fish = 6']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v)
    1
    >>> ini['cow']['something']
    1
    >>> ini['ob']['fish']
    3
    >>> ini['bo']['fish']
    6
    """

    
def _unexpected_validation_errors():
    """
    Although the input is nonsensical we should not crash but correctly 
    report the failure to validate
    
    # section specified, got scalar
    >>> from configobj.validate import ValidateError 
    >>> s = ['[cow]', 'something = boolean']
    >>> c = ['cow = true']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v)
    0

    >>> ini = ConfigObj(c, configspec=s)
    >>> res = ini.validate(v, preserve_errors=True)
    >>> check = flatten_errors(ini, res)
    >>> for entry in check:
    ...     isinstance(entry[2], ValidateError)
    ...     print(str(entry[2]))
    True
    Section 'cow' was provided as a single value
    

    # scalar specified, got section
    >>> s = ['something = boolean']
    >>> c = ['[something]', 'cow = true']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v)
    0
    
    >>> ini = ConfigObj(c, configspec=s)
    >>> res = ini.validate(v, preserve_errors=True)
    >>> check = flatten_errors(ini, res)
    >>> for entry in check:
    ...     isinstance(entry[2], ValidateError)
    ...     print(str(entry[2]))
    True
    Value 'something' was provided as a section
    
    # unexpected section
    >>> s = []
    >>> c = ['[cow]', 'dog = true']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v)
    1
    
    
    >>> s = ['[cow]', 'dog = boolean']
    >>> c = ['[cow]', 'dog = true']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> ini.validate(v, preserve_errors=True)
    1
    """
    
def _test_pickle():
    """
    >>> import pickle
    >>> s = ['[cow]', 'dog = boolean']
    >>> c = ['[cow]', 'dog = true']
    >>> ini = ConfigObj(c, configspec=s)
    >>> v = Validator()
    >>> string = pickle.dumps(ini)
    >>> new = pickle.loads(string)
    >>> new.validate(v)
    1
    """

def _test_as_list():
    """
    >>> a = ConfigObj()
    >>> a['a'] = 1
    >>> a.as_list('a')
    [1]
    >>> a['a'] = (1,)
    >>> a.as_list('a')
    [1]
    >>> a['a'] = [1]
    >>> a.as_list('a')
    [1]
    """

def _test_list_interpolation():
    """
    >>> c = ConfigObj()
    >>> c['x'] = 'foo'
    >>> c['list'] = ['%(x)s', 3]
    >>> c['list']
    ['foo', 3]
    """

def _test_extra_values():
    """
    >>> spec = ['[section]']
    >>> infile = ['bar = 3', '[something]', 'foo = fish', '[section]', 'foo=boo']
    >>> c = ConfigObj(infile, configspec=spec)
    >>> c.extra_values
    []
    >>> c.extra_values = ['bar', 'gosh', 'what']
    >>> c.validate(Validator())
    1
    >>> c.extra_values
    ['bar', 'something']
    >>> c['section'].extra_values
    ['foo']
    >>> c['something'].extra_values
    []
    """

def _test_reset_and_clear_more():
    """
    >>> c = ConfigObj()
    >>> c.extra_values = ['foo']
    >>> c.defaults = ['bar']
    >>> c.default_values = {'bar': 'baz'}
    >>> c.clear()
    >>> c.defaults
    []
    >>> c.extra_values
    []
    >>> c.default_values
    {'bar': 'baz'}
    >>> c.extra_values = ['foo']
    >>> c.defaults = ['bar']
    >>> c.reset()
    >>> c.defaults
    []
    >>> c.extra_values
    []
    >>> c.default_values
    {}
    """

def _test_invalid_lists():
    """
    >>> v = ['string = val, val2, , val3']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = val, val2,, val3']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = val, val2,,']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = val, ,']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = val, ,  ']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = ,,']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = ,, ']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = ,foo']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    >>> v = ['string = foo, ']
    >>> c = ConfigObj(v)
    >>> c['string']
    ['foo']
    >>> v = ['string = foo, "']
    >>> c = ConfigObj(v)
    Traceback (most recent call last):
    ParseError: Parse error in value at line 1.
    """

def _test_validation_with_preserve_errors():
    """
    >>> v = Validator()
    >>> spec = ['[section]', 'foo = integer']
    >>> c = ConfigObj(configspec=spec)
    >>> c.validate(v, preserve_errors=True)
    {'section': False}
    >>> c = ConfigObj(['[section]'], configspec=spec)
    >>> c.validate(v)
    False
    >>> c.validate(v, preserve_errors=True)
    {'section': {'foo': False}}
    """


# test _created on Section

# TODO: Test BOM handling
# TODO: Test error code for badly built multiline values
# TODO: Test handling of StringIO
# TODO: Test interpolation with writing


if __name__ == '__main__':
    # run the code tests in doctest format
    #
    testconfig1 = """\
    key1= val    # comment 1
    key2= val    # comment 2
    # comment 3
    [lev1a]     # comment 4
    key1= val    # comment 5
    key2= val    # comment 6
    # comment 7
    [lev1b]    # comment 8
    key1= val    # comment 9
    key2= val    # comment 10
    # comment 11
        [[lev2ba]]    # comment 12
        key1= val    # comment 13
        # comment 14
        [[lev2bb]]    # comment 15
        key1= val    # comment 16
    # comment 17
    [lev1c]    # comment 18
    # comment 19
        [[lev2c]]    # comment 20
        # comment 21
            [[[lev3c]]]    # comment 22
            key1 = val    # comment 23"""
    #
    testconfig2 = b"""\
                        key1 = 'val1'
                        key2 =   "val2"
                        key3 = val3
                        ["section 1"] # comment
                        keys11 = val1
                        keys12 = val2
                        keys13 = val3
                        [section 2]
                        keys21 = val1
                        keys22 = val2
                        keys23 = val3
                        
                            [['section 2 sub 1']]
                            fish = 3
    """
    #
    testconfig6 = b'''
    name1 = """ a single line value """ # comment
    name2 = \''' another single line value \''' # comment
    name3 = """ a single line value """
    name4 = \''' another single line value \'''
        [ "multi section" ]
        name1 = """
        Well, this is a
        multiline value
        """
        name2 = \'''
        Well, this is a
        multiline value
        \'''
        name3 = """
        Well, this is a
        multiline value
        """     # a comment
        name4 = \'''
        Well, this is a
        multiline value
        \'''  # I guess this is a comment too
    '''
    #
    # these cannot be put among the doctests, because the doctest module
    # does a string.expandtabs() on all of them, sigh
    # oneTabCfg = ['[sect]', '\t[[sect]]', '\t\tfoo = bar']
    # twoTabsCfg = ['[sect]', '\t\t[[sect]]', '\t\t\t\tfoo = bar']
    # tabsAndSpacesCfg = [b'[sect]', b'\t \t [[sect]]', b'\t \t \t \t foo = bar']
    #
    import doctest
    m = sys.modules.get('__main__')
    globs = m.__dict__.copy()
    a = ConfigObj(testconfig1.split('\n'), raise_errors=True)
    b = ConfigObj(testconfig2.split(b'\n'), raise_errors=True)
    i = ConfigObj(testconfig6.split(b'\n'), raise_errors=True)
    globs.update({'a': a, 'b': b, 'i': i})
    pre_failures, pre_tests = doctest.testmod(
        m, globs=globs,
        optionflags=doctest.IGNORE_EXCEPTION_DETAIL | doctest.ELLIPSIS)

    import configobj
    post_failures, post_tests = doctest.testmod(
        configobj, globs=globs,
        optionflags=doctest.IGNORE_EXCEPTION_DETAIL | doctest.ELLIPSIS)
    assert not (pre_failures or post_failures), (
        '{} failures out of {} tests'.format(post_failures + pre_failures,
                                             post_tests + pre_tests))


# Man alive I prefer unittest ;-)
