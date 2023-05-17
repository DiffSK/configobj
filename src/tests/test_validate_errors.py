import os

import pytest

from configobj import ConfigObj, get_extra_values, ParseError, NestingError
from configobj.validate import Validator, VdtUnknownCheckError

@pytest.fixture()
def thisdir():
    return os.path.dirname(os.path.join(os.getcwd(), __file__))


@pytest.fixture()
def inipath(thisdir):
    return os.path.join(thisdir, 'conf.ini')


@pytest.fixture()
def specpath(thisdir):
    return os.path.join(thisdir, 'conf.spec')


@pytest.fixture()
def conf(inipath, specpath):
    return ConfigObj(inipath, configspec=specpath)


def test_validate_no_valid_entries(conf):
    validator = Validator()
    result = conf.validate(validator)
    assert not result


def test_validate_preserve_errors(conf):
    validator = Validator()
    result = conf.validate(validator, preserve_errors=True)

    assert not result['value']
    assert not result['missing-section']

    section = result['section']
    assert not section['value']
    assert not section['sub-section']['value']
    assert not section['missing-subsection']


def test_validate_extra_values(conf):
    conf.validate(Validator(), preserve_errors=True)

    assert conf.extra_values == ['extra', 'extra-section']
    assert conf['section'].extra_values == ['extra-sub-section']
    assert conf['section']['sub-section'].extra_values == ['extra']


def test_get_extra_values(conf):
    conf.validate(Validator(), preserve_errors=True)
    extra_values = get_extra_values(conf)

    expected = sorted([
        ((), 'extra'),
        ((), 'extra-section'),
        (('section', 'sub-section'), 'extra'),
        (('section',), 'extra-sub-section'),
    ])
    assert sorted(extra_values) == expected


def test_invalid_lines_with_percents(tmpdir, specpath):
    ini = tmpdir.join('config.ini')
    ini.write('extra: %H:%M\n')
    with pytest.raises(ParseError):
        conf = ConfigObj(str(ini), configspec=specpath, file_error=True)


def test_no_parent(tmpdir, specpath):
    ini = tmpdir.join('config.ini')
    ini.write('[[haha]]')
    with pytest.raises(NestingError):
        conf = ConfigObj(str(ini), configspec=specpath, file_error=True)


def test_re_dos(val):
    value = "aaa"
    i = 165100
    attack = '\x00'*i + ')' + '('*i
    with pytest.raises(VdtUnknownCheckError):
        val.check(attack, value)
