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

if sys.version_info < (2, 6):
    print('for python versions < 2.6 use configobj '
          'version 4.7.2')
    sys.exit(1)

__here__ = os.path.abspath(os.path.dirname(__file__))

NAME = 'configobj'
MODULES = []
PACKAGES = ['configobj']
DESCRIPTION = 'Config file reading, writing and validation.'
URL = 'https://github.com/DiffSK/configobj'

REQUIRES = """
    six
"""

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
    print("WARNING: Cannot open/read CHANGES.rst due to {0}".format(exc))

CLASSIFIERS = [
    # Details at http://pypi.python.org/pypi?:action=list_classifiers
    'Development Status :: 6 - Mature',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Rob Dennis, Eli Courtwright (Michael Foord & Nicola Larosa original maintainers)'

AUTHOR_EMAIL = 'rdennis+configobj@gmail.com, eli@courtwright.org, fuzzyman@voidspace.co.uk, nico@tekNico.net'

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
    install_requires=[i.strip() for i in REQUIRES.splitlines() if i.strip()],
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    license='BSD (2 clause)',
)

if __name__ == '__main__':
    setup(**project)
