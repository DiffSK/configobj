# configobj
[![Build Status](https://travis-ci.org/DiffSK/configobj.svg?branch=master)](https://travis-ci.org/DiffSK/configobj)
[![Coverage Status](https://img.shields.io/coveralls/DiffSK/configobj.svg)](https://coveralls.io/r/DiffSK/configobj?branch=master)
[![PyPI version](http://img.shields.io/pypi/v/configobj.svg)](https://pypi.python.org/pypi/configobj)
[![Downloads](https://img.shields.io/pypi/dw/configobj.svg)](https://pypi.python.org/pypi/configobj)
[![License](https://img.shields.io/badge/license-BSD_3--clause-red.svg)](https://github.com/DiffSK/configobj/blob/master/LICENSE)


Python 3+ compatible port of the [configobj](https://pypi.python.org/pypi/configobj/) library.


## Documentation

You can find a full manual at [readthedocs](http://configobj.readthedocs.org/).


## Status

This project is now maintained by [Eli Courtwright](https://github.com/EliAndrewC) and [Rob Dennis](https://github.com/robdennis) with the blessing of original creator [Michael Foord](http://www.voidspace.org.uk/).

For long time ConfigObj users, the biggest change is in the officially supported Python versions:
- 2.6
- 2.7
- 3.3
- 3.4

(notably adding Python 3 support; previously this was 2.3 - 2.6)
Other versions may work, but this is what travis and tox uses to run the tests on commit.


## Roadmap

- Fixing any issues introduced as a result of the added Python 3 support
- Moving tests away from doctests in favor of pytest (reasonable now that versions older than 2.6 are dropped)
- Considering new features that work in a backwards-compatible way (feel free to open an issue with your suggestion)


## Contributing

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See [CONTRIBUTING](https://github.com/DiffSK/configobj/blob/master/CONTRIBUTING.md) for more.

As a documentation author or developer,
to create a working directory for this project,
call these commands:

```sh
git clone "https://github.com/DiffSK/configobj.git"
cd "configobj"
. .env --yes --develop
invoke build --docs test check
```

To start a watchdog that auto-rebuilds documentation and reloads the opened browser tab on any change,
call ``invoke docs -w -b`` (stop the watchdog using the ``-k`` option).

You might also need to follow some
[setup procedures](https://py-generic-project.readthedocs.org/en/latest/installing.html#quick-setup)
to make the necessary basic commands available on *Linux*, *Mac OS X*, and *Windows*.
