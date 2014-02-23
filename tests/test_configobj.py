from codecs import BOM_UTF8
from warnings import catch_warnings

import pytest
import six

from configobj import ConfigObj, flatten_errors
from validate import Validator, VdtValueTooSmallError

def test_order_preserved():
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
    assert c2.scalars == ['a', 'b', 'c']
    assert c2.sections == ['section', 'section2', 'section3']
    assert c2['section'].scalars == ['a', 'b', 'c']
    assert c2['section'].sections == ['section', 'section2', 'section3']

    assert c['section'] is not c2['section']
    assert c['section']['section'] is not c2['section']['section']


def test_options_deprecation():
    with catch_warnings(record=True) as log:
        ConfigObj(options={})

    # unpack the only member of log
    try:
        warning, = log
    except ValueError:
        assert len(log) == 1

    assert warning.category == DeprecationWarning


def test_list_members():
    c = ConfigObj()
    c['a'] = []
    c['a'].append('foo')
    assert c['a'] == ['foo']


def test_list_interpolation_with_pop():
    c = ConfigObj()
    c['a'] = []
    c['a'].append('%(b)s')
    c['b'] = 'bar'
    assert c.pop('a') == ['bar']


def test_with_default():
    c = ConfigObj()
    c['a'] = 3

    assert c.pop('a') == 3
    assert c.pop('b', 3) == 3
    with pytest.raises(KeyError):
        c.pop('c')


def test_interpolation_with_section_names():
    cfg = """
item1 = 1234
[section]
    [[item1]]
    foo='bar'
    [[DEFAULT]]
        [[[item1]]]
        why = would you do this?
    [[other-subsection]]
    item2 = '$item1'""".splitlines()
    c = ConfigObj(cfg, interpolation='Template')

    # This raises an exception in 4.7.1 and earlier due to the section
    # being found as the interpolation value
    repr(c)


def test_interoplation_repr():
    c = ConfigObj(['foo = $bar'], interpolation='Template')
    c['baz'] = {}
    c['baz']['spam'] = '%(bar)s'

    # This raises a MissingInterpolationOption exception in 4.7.1 and earlier
    repr(c)


#issue #18
def test_unicode_conversion_when_encoding_is_set():
    cfg = """
test = some string
    """.splitlines()

    c = ConfigObj(cfg, encoding='utf8')

    if six.PY2:
        assert not isinstance(c['test'], str)
        assert isinstance(c['test'], unicode)
    else:
        assert isinstance(c['test'], str)


#issue #18
def test_no_unicode_conversion_when_encoding_is_omitted():
    cfg = """
test = some string
    """.splitlines()

    c = ConfigObj(cfg)
    if six.PY2:
        assert isinstance(c['test'], str)
        assert not isinstance(c['test'], unicode)
    else:
        assert isinstance(c['test'], str)


@pytest.fixture
def testconfig1():
    """
    copied from the main doctest
    """
    return """\
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


@pytest.fixture
def testconfig2():
    return """\
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

@pytest.fixture
def a(testconfig1):
    """
    also copied from main doc tests
    """
    return ConfigObj(testconfig1.split('\n'), raise_errors=True)


@pytest.fixture
def b(testconfig2):
    """
    also copied from main doc tests
    """
    return ConfigObj(testconfig2.split('\n'), raise_errors=True)


def test_configobj_dict_representation(a, b):

    assert a.depth == 0
    assert a == {
        'key2': 'val',
        'key1': 'val',
        'lev1c': {
            'lev2c': {
                'lev3c': {
                    'key1': 'val',
                    },
                },
            },
        'lev1b': {
            'key2': 'val',
            'key1': 'val',
            'lev2ba': {
                'key1': 'val',
                },
            'lev2bb': {
                'key1': 'val',
                },
            },
        'lev1a': {
            'key2': 'val',
            'key1': 'val',
            },
        }
    
    assert b.depth == 0
    assert b == {
        'key3': 'val3',
        'key2': 'val2',
        'key1': 'val1',
        'section 1': {
            'keys11': 'val1',
            'keys13': 'val3',
            'keys12': 'val2',
            },
        'section 2': {
            'section 2 sub 1': {
                'fish': '3',
                },
            'keys21': 'val1',
            'keys22': 'val2',
            'keys23': 'val3',
            },
        }

    t = '''
        'a' = b # !"$%^&*(),::;'@~#= 33
        "b" = b #= 6, 33
''' .split('\n')
    t2 = ConfigObj(t)
    assert t2 == {'a': 'b', 'b': 'b'}
    t2.inline_comments['b'] = ''
    del t2['a']
    assert t2.write() == ['','b = b', '']


def test_behavior_when_list_values_is_false():
    c = '''
       key1 = no quotes
       key2 = 'single quotes'
       key3 = "double quotes"
       key4 = "list", 'with', several, "quotes"
       '''
    cfg = ConfigObj(c.splitlines(), list_values=False)
    assert cfg == {
        'key1': 'no quotes',
        'key2': "'single quotes'",
        'key3': '"double quotes"',
        'key4': '"list", \'with\', several, "quotes"'
    }

    cfg2 = ConfigObj(list_values=False)
    cfg2['key1'] = 'Multiline\nValue'
    cfg2['key2'] = '''"Value" with 'quotes' !'''
    assert cfg2.write() == [
        "key1 = '''Multiline\nValue'''",
        'key2 = "Value" with \'quotes\' !'
    ]

    cfg2.list_values = True
    assert cfg2.write() == [
        "key1 = '''Multiline\nValue'''",
        'key2 = \'\'\'"Value" with \'quotes\' !\'\'\''
    ]


def test_flatten_errors():
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
    '''.split('\n')
    configspec = '''
       test1= integer(30,50)
       test2= string
       test3=integer
       test4=float(6.0)
       [section]
           test1=integer(30,50)
           test2=string
           test3=integer
           test4=float(6.0)
           [[sub section]]
               test1=integer(30,50)
               test2=string
               test3=integer
               test4=float(6.0)
       '''.split('\n')
    val = Validator()
    c1 = ConfigObj(config, configspec=configspec)
    res = c1.validate(val)
    assert flatten_errors(c1, res) == [([], 'test4', False), (['section'], 'test4', False), (['section', 'sub section'], 'test4', False)]
    res = c1.validate(val, preserve_errors=True)
    check = flatten_errors(c1, res)
    assert check[0][:2] == ([], 'test4')
    assert check[1][:2] == (['section'], 'test4')
    assert check[2][:2] == (['section', 'sub section'], 'test4')
    for entry in check:
        assert isinstance(entry[2], VdtValueTooSmallError)
        assert str(entry[2]) == 'the value "5.0" is too small.'


def test_unicode_handling():
    u_base = '''
    # initial comment
       # inital comment 2
    test1 = some value
    # comment
    test2 = another value    # inline comment
    # section comment
    [section]    # inline comment
       test = test    # another inline comment
       test2 = test2
    # final comment
    # final comment2
    '''

    u = u_base.encode('utf_8').splitlines(True)
    u[0] = BOM_UTF8 + u[0]
    uc = ConfigObj(u)
    uc.encoding = None
    assert uc.BOM
    assert uc == {'test1': 'some value', 'test2': 'another value',
                  'section': {'test': 'test', 'test2': 'test2'}}
    uc = ConfigObj(u, encoding='utf_8', default_encoding='latin-1')
    assert uc.BOM
    assert isinstance(uc['test1'], six.text_type)
    assert uc.encoding == 'utf_8'
    assert uc.newlines == '\n'
    assert len(uc.write()) == 13
    uc['latin1'] = "This costs lot's of "
    a_list = uc.write()
    assert 'latin1' in str(a_list)
    assert len(a_list) == 14
    assert isinstance(a_list[0], six.binary_type)
    assert a_list[0].startswith(BOM_UTF8)

    u = u_base.replace('\n', '\r\n').encode('utf-8').splitlines(True)
    uc = ConfigObj(u)
    assert uc.newlines == '\r\n'
    uc.newlines = '\r'
    file_like = six.StringIO()
    uc.write(file_like)
    file_like.seek(0)
    uc2 = ConfigObj(file_like)
    assert uc2 == uc
    assert uc2.filename == None
    assert uc2.newlines == '\r'


def _doctest():
    """
    Dummy function to hold some of the doctests.

    Test flatten_errors:

    Test unicode handling, BOM, write witha file like object and line endings :



    Test validate in copy mode
    a = '''
    # Initial Comment
    ...
    key1 = string(default=Hello)
    ...
    # section comment
    [section] # inline comment
    # key1 comment
    key1 = integer(default=6)
    # key2 comment
    key2 = boolean(default=True)
    ...
       # subsection comment
       [[sub-section]] # inline comment
       # another key1 comment
       key1 = float(default=3.0)'''.splitlines()
    b = ConfigObj(configspec=a)
    b.validate(val, copy=True)
    1
    b.write() == ['',
    '# Initial Comment',
    '',
    'key1 = Hello',
    '',
    '# section comment',
    '[section]    # inline comment',
    '    # key1 comment',
    '    key1 = 6',
    '    # key2 comment',
    '    key2 = True',
    '    ',
    '    # subsection comment',
    '    [[sub-section]]    # inline comment',
    '        # another key1 comment',
    '        key1 = 3.0']
    1

    Test Writing Empty Values
    a = '''
       key1 =
       key2 =# a comment'''
    b = ConfigObj(a.splitlines())
    b.write()
    ['', 'key1 = ""', 'key2 = ""    # a comment']
    b.write_empty_values = True
    b.write()
    ['', 'key1 = ', 'key2 =     # a comment']

    Test unrepr when reading
    a = '''
       key1 = (1, 2, 3)    # comment
       key2 = True
       key3 = 'a string'
       key4 = [1, 2, 3, 'a mixed list']
    '''.splitlines()
    b = ConfigObj(a, unrepr=True)
    b == {'key1': (1, 2, 3),
    'key2': True,
    'key3': 'a string',
    'key4': [1, 2, 3, 'a mixed list']}
    1

    Test unrepr when writing
    c = ConfigObj(b.write(), unrepr=True)
    c == b
    1

    Test unrepr with multiline values
    a = '''k = \"""{
    'k1': 3,
    'k2': 6.0}\"""
    '''.splitlines()
    c = ConfigObj(a, unrepr=True)
    c == {'k': {'k1': 3, 'k2': 6.0}}
    1

    Test unrepr with a dictionary
    a = 'k = {"a": 1}'.splitlines()
    c = ConfigObj(a, unrepr=True)
    isinstance(c['k'], dict)
    True

    a = ConfigObj()
    a['a'] = 'fish'
    a.as_bool('a')
    Traceback (most recent call last):
    ValueError: Value "fish" is neither True nor False
    a['b'] = 'True'
    a.as_bool('b')
    1
    a['b'] = 'off'
    a.as_bool('b')
    0

    a = ConfigObj()
    a['a'] = 'fish'
    try:
       a.as_int('a')
    except ValueError as e:
       err_mess = str(e)
    err_mess.startswith('invalid literal for int()')
    1
    a['b'] = '1'
    a.as_int('b')
    1
    a['b'] = '3.2'
    try:
       a.as_int('b')
    except ValueError as e:
       err_mess = str(e)
    err_mess.startswith('invalid literal for int()')
    1

    a = ConfigObj()
    a['a'] = 'fish'
    a.as_float('a')
    Traceback (most recent call last):
    ValueError: invalid literal for float(): fish
    a['b'] = '1'
    a.as_float('b')
    1.0
    a['b'] = '3.2'
    a.as_float('b')
    3.2...

     Test # with unrepr
     a = '''
        key1 = (1, 2, 3)    # comment
        key2 = True
        key3 = 'a string'
        key4 = [1, 2, 3, 'a mixed list#']
     '''.splitlines()
     b = ConfigObj(a, unrepr=True)
     b == {'key1': (1, 2, 3),
     'key2': True,
     'key3': 'a string',
     'key4': [1, 2, 3, 'a mixed list#']}
     1
    """

    # Comments are no longer parsed from values in configspecs
    # so the following test fails and is disabled
    untested = """
    Test validate in copy mode
    a = '''
    # Initial Comment
    ...
    key1 = string(default=Hello)    # comment 1
    ...
    # section comment
    [section] # inline comment
    # key1 comment
    key1 = integer(default=6) # an integer value
    # key2 comment
    key2 = boolean(default=True) # a boolean
    ...
       # subsection comment
       [[sub-section]] # inline comment
       # another key1 comment
       key1 = float(default=3.0) # a float'''.splitlines()
    b = ConfigObj(configspec=a)
    b.validate(val, copy=True)
    1
    b.write()
    b.write() == ['',
    '# Initial Comment',
    '',
    'key1 = Hello    # comment 1',
    '',
    '# section comment',
    '[section]    # inline comment',
    '    # key1 comment',
    '    key1 = 6    # an integer value',
    '    # key2 comment',
    '    key2 = True    # a boolean',
    '    ',
    '    # subsection comment',
    '    [[sub-section]]    # inline comment',
    '        # another key1 comment',
    '        key1 = 3.0    # a float']
    1
    """
