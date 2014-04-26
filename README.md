configobj [![Build Status](https://travis-ci.org/DiffSK/configobj.svg?branch=master)](https://travis-ci.org/DiffSK/configobj)[![Downloads](https://pypip.in/d/configobj/badge.png)](https://crate.io/packages/configobj)[![PyPI version](https://badge.fury.io/py/configobj.png)](http://badge.fury.io/py/configobj)[![Coverage Status](https://coveralls.io/repos/DiffSK/configobj/badge.png?branch=master)](https://coveralls.io/r/DiffSK/configobj?branch=master)
=========

Python 3+ compatible port of the [configobj](https://pypi.python.org/pypi/configobj/) library.

Documentation
=========
Found at [readthedocs](http://configobj.readthedocs.org/)

Status
=========
This project is now maintained by [Eli Courtwright](https://github.com/EliAndrewC) and [Rob Dennis](https://github.com/robdennis) with the blessing of original creator [Michael Foord](http://www.voidspace.org.uk/).

For long time ConfigObj users, the biggest change is in the officially supported python versions:
- 2.6
- 2.7
- 3.2
- 3.3

(notably adding python 3 support; previously this was 2.3 - 2.6)
Other versions may work, but this is what travis and tox uses to run the tests on commit.

Roadmap
=========
- Fixing any issues introduced as a result of the added python 3 support
- Moving tests away from doctests in favor of pytest (reasonable now that versions older than 2.6 are dropped)
- Considering new features that work in a backwards-compatible way (feel free to open an issue with your suggestion)
