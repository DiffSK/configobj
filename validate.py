# validate.py
# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import
#
# A Validator object (deprecation shim)
#
# Copyright (C) 2005-2014:
# (name) : (email)
# Michael Foord: fuzzyman AT voidspace DOT org DOT uk
# Mark Andrews: mark AT la-la DOT com
# Nicola Larosa: nico AT tekNico DOT net
# Rob Dennis: rdennis AT gmail DOT com
# Eli Courtwright: eli AT courtwright DOT org

# This software is licensed under the terms of the BSD license.
# http://opensource.org/licenses/BSD-3-Clause

# ConfigObj 5 - main repository for documentation and issue tracking:
# https://github.com/DiffSK/configobj

"""
    The Validator object is used to check that supplied values
    conform to a specification.

    This is the DEPRECATED top-level module shim, that imports
    the validator from the new location ``configobj.validate``.
"""
from __future__ import absolute_import, unicode_literals

import warnings

from configobj.validate import *

# version of the shim, just to satisfy the old API surface
__version__ = '1.1.0'

warnings.warn("top-level 'validate' moved to 'configobj.validate',"
              " please adapt your imports", ImportWarning)
