#!/usr/bin/env python
# setup.py
# Install script for ConfigObj
# Copyright (C) 2005-2014:
# (name) : (email)
# Michael Foord: fuzzyman AT voidspace DOT org DOT uk
# Mark Andrews: mark AT la-la DOT com
# Nicola Larosa: nico AT tekNico DOT net
# Rob Dennis: rdennis AT gmail DOT com
# Eli Courtwright: eli AT courtwright DOT org

# This software is licensed under the terms of the BSD license.
# http://opensource.org/licenses/BSD-3-Clause
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
MODULES = ['validate']
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
It has lots of other features though :

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

| Release 5.0.6 improves error messages in certain edge cases
| Release 5.0.5 corrects a unicode-bug that still existed in writing files
| Release 5.0.4 corrects a unicode-bug that still existed in reading files after
| fixing lists of string in 5.0.3
| Release 5.0.3 corrects errors related to the incorrectly handling unicode
| encoding and writing out files
| Release 5.0.2 adds a specific error message when trying to install on
| Python versions older than 2.5
| Release 5.0.1 fixes a regression with unicode conversion not happening
| in certain cases PY2
| Release 5.0.0 updates the supported Python versions to 2.6, 2.7, 3.2, 3.3
| and is otherwise unchanged
| Release 4.7.2 fixes several bugs in 4.7.1
| Release 4.7.1 fixes a bug with the deprecated options keyword in
| 4.7.0.
| Release 4.7.0 improves performance adds features for validation and
| fixes some bugs."""

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
)

if __name__ == '__main__':
    setup(**project)
