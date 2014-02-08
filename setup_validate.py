# setup.py
# Install script for validate
# Copyright (C) 2005-2014:
# (name) : (email)
# Michael Foord: fuzzyman AT voidspace DOT org DOT uk
# Mark Andrews: mark AT la-la DOT com
# Nicola Larosa: nico AT tekNico DOT net
# Rob Dennis: rdennis AT gmail DOT com
# Eli Courtwright: eli AT courtwright DOT org

# This software is licensed under the terms of the BSD license.
# http://opensource.org/licenses/BSD-3-Clause

import sys
from distutils.core import setup
from validate import __version__ as VERSION

NAME = 'validate'

MODULES = 'validate',

DESCRIPTION = 'Config file reading, writing, and validation.'

URL = 'http://www.voidspace.org.uk/python/validate.html'

DOWNLOAD_URL = "http://www.voidspace.org.uk/downloads/validate.py"

LONG_DESCRIPTION = """`validate.py <http://www.voidspace.org.uk/python/validate.html>`_ is a
module for validating values against a specification. It can be used
with `ConfigObj <http://www.voidspace.org.uk/python/configobj.html>`_, or as a
standalone module.

It is extensible, and as well as doing type conversion from strings,
you can easily implement your own functions for transforming values in
any way you please."""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Michael Foord'

AUTHOR_EMAIL = 'fuzzyman@voidspace.org.uk'

KEYWORDS = "validation, schema, conversion, checking, configobj, config, configuration".split(', ')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      download_url=DOWNLOAD_URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      py_modules=MODULES,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
     )
