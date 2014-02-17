import os
from configobj import ConfigObj

import pytest

try:
    #TODO(robdennis): determine if this is really 2.6 and newer
    # Python 2.6 only
    from warnings import catch_warnings
except ImportError:
    # this will cause an error, but at least the other tests
    # will run on Python 2.5
    catch_warnings = None


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


@pytest.mark.skipif(catch_warnings is None,
                    reason='catch_warnings is required')
def test_options_deprecation():
    with catch_warnings(record=True) as log:
        ConfigObj(options={})

    # unpack the only member of log
    warning, = log
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

