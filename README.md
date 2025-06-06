# configobj
[![Coverage Status](https://img.shields.io/coveralls/DiffSK/configobj.svg)](https://coveralls.io/r/DiffSK/configobj?branch=master)
[![PyPI version](http://img.shields.io/pypi/v/configobj.svg)](https://pypi.python.org/pypi/configobj)
[![License](https://img.shields.io/badge/license-BSD_3--clause-red.svg)](https://github.com/DiffSK/configobj/blob/master/LICENSE)


Python 3+ compatible port of the [configobj](https://pypi.python.org/pypi/configobj/) library.

The Github CI/CD Pipeline runs tests on python versions:
- 3.8
- 3.9
- 3.10
- 3.11
- 3.12
- 3.13


## Documentation

You can find a full manual on how to use ConfigObj at [readthedocs](http://configobj.readthedocs.io/).

## Status

This is a mature project that is not actively maintained at this time.

## Branches

The default branch of this repository is the [`release` branch](https://github.com/DiffSK/configobj/tree/release),
rather than the [`master` branch](https://github.com/DiffSK/configobj/tree/master).
This decision dates back to when this project moved from being actively
maintained to it's current state as a mature project.
At that time (in 2023), [changes introduced](https://github.com/DiffSK/configobj/compare/v5.0.6...master)
into the `master` branch had not been fully integrated, and the tooling had
shifted in ways that made [continuing from `master` unclear](https://github.com/DiffSK/configobj/pull/237#issuecomment-1925401612).

Instead, [we chose to continue development](https://github.com/DiffSK/configobj/issues/213#issuecomment-1377686121)
from the `5.0.6` release branch. Any changes made to master after that release
were effectively abandoned, and the `release` branch has served as the main
line of development since.

As a result, going forward, new pull requests should be made against the
`release` branch as the `master` branch is frozen in time.

## Past Contributors:

- [Michael Foord](https://agileabstractions.com/)
  - original creator of ``configobj`` and ``validate`` and maintainer through version 4
- [Rob Dennis](https://github.com/robdennis)
  - released version 5 (first python 3-compatible release) in 2014, bringing the project to github
  - released the last maintenance release (until new maintainership is established) in 2023
- [Eli Courtwright](https://github.com/EliAndrewC)
  - released version 5 (first python 3-compatible release) in 2014
- [Nicola Larosa](https://pypi.org/user/tekNico/)
  - Contributions to the pre-version 5 codebase 
- [Jürgen Hermann](https://github.com/jhermann)
  - day-to-day maintenance of the repo
