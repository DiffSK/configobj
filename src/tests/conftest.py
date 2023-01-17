# coding=utf-8
import pytest

from configobj import ConfigObj
from configobj.validate import Validator

@pytest.fixture
def empty_cfg():
    return ConfigObj()


@pytest.fixture
def val():
    return Validator()
