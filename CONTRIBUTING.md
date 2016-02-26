# Contribution Guidelines

## Overview

Contributing to this project is easy, and reporting an issue or adding to the documentation
also improves things for every user. You don't need to be a developer to contribute.


### Reporting issues

Please use the *GitHub issue tracker*, and describe your problem so that it can be easily
reproduced. Providing relevant version information on the project itself and your environment helps with that.


### Improving documentation

The easiest way to provide examples or related documentation that helps other users
is the *GitHub wiki*.

If you are comfortable with the Sphinx documentation tool, you can also prepare a
pull request with changes to the core documentation.
GitHub's built-in text editor makes this especially easy, when you choose the
_“Create a new branch for this commit and start a pull request”_ option on saving.
Small fixes for typos and the like are a matter of minutes when using that tool.


### Code contributions

Here's a quick guide to improve the code:

1. Fork the repo, and clone the fork to your machine.
1. Add your improvements, the technical details are further below.
1. Run the tests and make sure they're passing (`invoke test`).
1. Check for violations of code conventions (`invoke check`).
1. Make sure the documentation builds without errors (`invoke build --docs`).
1. Push to your fork and submit a [pull request](https://help.github.com/articles/using-pull-requests/).

Please be patient while waiting for a review. Life & work tend to interfere.


## Details on contributing code

This project is written in [Python](http://www.python.org/),
and the documentation is generated using [Sphinx](https://pypi.python.org/pypi/Sphinx).
[setuptools](https://packaging.python.org/en/latest/projects.html#setuptools)
and [Invoke](http://www.pyinvoke.org/) are used to build and manage the project.
Tests are written and executed using [pytest](http://pytest.org/) and
[tox](https://testrun.org/tox/ ).


### Set up a working development environment

To set up a working directory from your own fork,
follow [these steps](https://github.com/DiffSK/configobj#contributing),
but replace the repository `https` URLs with SSH ones that point to your fork.

For that to work on Debian type systems, you need the
`git`, `python`, and `python-virtualenv`
packages installed. Other distributions are similar.


### Add your changes to a feature branch

For any cohesive set of changes, create a *new* branch based on the current upstream `master`,
with a name reflecting the essence of your improvement.

```sh
git branch "name-for-my-fixes" origin/master
git checkout "name-for-my-fixes"
… make changes…
invoke ci # check output for broken tests, or PEP8 violations and the like
… commit changes…
git push origin "name-for-my-fixes"
```

Please don't create large lumps of unrelated changes in a single pull request.
Also take extra care to avoid spurious changes, like mass whitespace diffs.
All Python sources use spaces to indent, not TABs.


### Make sure your changes work

Some things that will increase the chance that your pull request is accepted:

* Follow style conventions you see used in the source already (and read [PEP8](http://pep8.org/)).
* Include tests that fail *without* your code, and pass *with* it. Only minor refactoring and documentation changes require no new tests. If you are adding functionality or fixing a bug, please also add a test for it!
* Update any documentation or examples impacted by your change.
* Styling conventions and code quality are checked with `invoke check`, tests are run using `invoke test`, and the docs can be built locally using `invoke build --docs`.

Following these hints also expedites the whole procedure, since it avoids unnecessary feedback cycles.
