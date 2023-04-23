# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods

import os

import pytest
import subprocess

@pytest.fixture()
def thisdir():
    return os.path.dirname(os.path.join(os.getcwd(), __file__))


def test_validate_template(thisdir,capsys):
    templatepath = os.path.join(thisdir, 'envsubst.ini.template')
    out = subprocess.check_output(["bash","-c","export SHELL=/bin/bash && python %s/conf_envsubst.py <(envsubst < %s)"%(thisdir,templatepath)])
    assert out.decode() == "{'shell': '/bin/bash'}\n"
