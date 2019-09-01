# configobj
[![Build Status](https://travis-ci.org/DiffSK/configobj.svg?branch=master)](https://travis-ci.org/DiffSK/configobj)
[![Coverage Status](https://img.shields.io/coveralls/DiffSK/configobj.svg)](https://coveralls.io/r/DiffSK/configobj?branch=master)
[![PyPI version](http://img.shields.io/pypi/v/configobj.svg)](https://pypi.python.org/pypi/configobj)
[![License](https://img.shields.io/badge/license-BSD_3--clause-red.svg)](https://github.com/DiffSK/configobj/blob/master/LICENSE)


Python 3+ compatible port of the [configobj](https://pypi.python.org/pypi/configobj/) library.


## Documentation

You can find a full manual on how to use ConfigObj at [readthedocs](http://configobj.readthedocs.io/).
If you want to *work on the project*, please see the [Contributing](#contributing) section below.


## Status

This project is now maintained by [Eli Courtwright](https://github.com/EliAndrewC) and [Rob Dennis](https://github.com/robdennis) with the blessing of original creator [Michael Foord](http://www.voidspace.org.uk/).

For long time ConfigObj users, the biggest change is in the officially supported Python versions (it *was* 2.3 … 2.6):

* 2.7
* 3.4 … 3.7

Other Python3 versions may work, but this is what *Travis* and ``tox`` use to run the tests on commit.


## Roadmap

- Fixing any issues introduced as a result of the added Python 3 support
- Moving tests away from doctests in favor of pytest (reasonable now that versions older than 2.6 are dropped)
- Considering new features that work in a backwards-compatible way (feel free to open an issue with your suggestion)
- Also see the [milestones](https://github.com/DiffSK/configobj/milestones)


## Contributing

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See [CONTRIBUTING](https://github.com/DiffSK/configobj/blob/master/CONTRIBUTING.md) for more.

As a documentation author or developer,
to **create a working directory** for this project,
call these commands:

```sh
git clone "https://github.com/DiffSK/configobj.git"
cd "configobj"
command . .env --yes --develop  # add '--virtualenv /usr/bin/virtualenv' for Python2
invoke build --docs test doctest check
```

For this to work, you might also need to follow some
[setup procedures](https://py-generic-project.readthedocs.io/en/latest/installing.html#quick-setup)
to make the necessary basic commands available on *Linux*, *Mac OS X*, and *Windows*.

**Running the test suite** can be done several ways, just call ``invoke test`` for a quick check.
Run ``invoke test.tox`` for testing with *all* supported Python versions
(if you [have them available](https://github.com/jhermann/priscilla/tree/master/pyenv)),
or be more selective by e.g. calling ``invoke test.tox -e py27,py34``.

Use ``invoke check`` to **run a code-quality scan**.

To **start a watchdog that auto-rebuilds documentation** and reloads the opened browser tab on any change,
call ``invoke docs -w -b`` (stop the watchdog using the ``-k`` option).
