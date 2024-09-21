#!/usr/bin/env python
# setup.py
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""Install script for ConfigObj"""

# Copyright (C) 2005-2014:
# (name) : (email)
# Michael Foord: fuzzyman AT voidspace DOT org DOT uk
# Mark Andrews: mark AT la-la DOT com
# Nicola Larosa: nico AT tekNico DOT net
# Rob Dennis: rdennis AT gmail DOT com
# Eli Courtwright: eli AT courtwright DOT org

# This software is licensed under the terms of the BSD license.
# http://opensource.org/licenses/BSD-3-Clause
import io
import os
import re
import sys
from contextlib import closing

from setuptools import setup

if sys.version_info[0] < 2:
    print('for Python versions < 3 use configobj '
          'version 5.0.8')
    sys.exit(1)

__here__ = os.path.abspath(os.path.dirname(__file__))

NAME = 'configobj'
MODULES = []
PACKAGES = ['configobj', 'validate']
DESCRIPTION = 'Config file reading, writing and validation.'
URL = 'https://github.com/DiffSK/configobj'

VERSION = ''
with closing(open(os.path.join(__here__, 'src', PACKAGES[0], '_version.py'), 'r')) as handle:
    for line in handle.readlines():
        if line.startswith('__version__'):
            VERSION = re.split('''['"]''', line)[1]
assert re.match(r"[0-9](\.[0-9]+)", VERSION), "No semantic version found in 'configobj._version'"

LONG_DESCRIPTION = """**ConfigObj** is a simple but powerful config file reader and writer: an *ini
file round tripper*. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files.

List of Features
----------------

* Nested sections (subsections), to any level
* List values
* Multiple line values
* Full Unicode support
* String interpolation (substitution)
* Integrated with a powerful validation system

    - including automatic type checking/conversion
    - and allowing default values
    - repeated sections

* All comments in the file are preserved
* The order of keys/sections is preserved
* Powerful ``unrepr`` mode for storing/retrieving Python data-types

"""

try:
    with io.open('CHANGES.rst', encoding='utf-8') as handle:
        LONG_DESCRIPTION += handle.read()
except EnvironmentError as exc:
    # Build / install anyway
    print("WARNING: Cannot open/read CHANGES.rst due to {}".format(exc))

CLASSIFIERS = [
    # Details at http://pypi.python.org/pypi?:action=list_classifiers
    'Development Status :: 6 - Mature',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Rob Dennis, Eli Courtwright (Michael Foord & Nicola Larosa original maintainers)'

AUTHOR_EMAIL = 'rdennis+configobj@gmail.com, eli@courtwright.org, michael@python.org, nico@tekNico.net'

KEYWORDS = "config, ini, dictionary, application, admin, sysadmin, configuration, validation".split(', ')

project = dict(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    py_modules=MODULES,
    package_dir={'': 'src'},
    packages=PACKAGES,
    python_requires='>=3.7',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    license='BSD-3-Clause',
)

if __name__ == '__main__':
    setup(**project)
