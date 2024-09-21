Changelog
---------

Release 5.0.9
"""""""""""""

* drop support for Python 2 and <3.7
* fix CVE-2023-26112, ReDoS attack

Release 5.0.8
"""""""""""""

* fixing/test for a regression introduced in 5.0.7 that prevented ``import validate`` from working


Release 5.0.7
"""""""""""""

* update testing to validate against python version 2.7 and 3.5-3.11
* update broken links / non-existent services and references

Older Releases
""""""""""""""

* Release 5.0.6 improves error messages in certain edge cases
* Release 5.0.5 corrects a unicode-bug that still existed in writing files
* Release 5.0.4 corrects a unicode-bug that still existed in reading files after
  fixing lists of string in 5.0.3
* Release 5.0.3 corrects errors related to the incorrectly handling unicode
  encoding and writing out files
* Release 5.0.2 adds a specific error message when trying to install on
  Python versions older than 2.5
* Release 5.0.1 fixes a regression with unicode conversion not happening
  in certain cases PY2
* Release 5.0.0 updates the supported Python versions to 2.6, 2.7, 3.2, 3.3
  and is otherwise unchanged
* Release 4.7.2 fixes several bugs in 4.7.1
* Release 4.7.1 fixes a bug with the deprecated options keyword in 4.7.0.
* Release 4.7.0 improves performance adds features for validation and
  fixes some bugs.
