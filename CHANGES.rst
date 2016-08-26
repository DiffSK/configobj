Changelog
---------

Release 5.1.0
"""""""""""""

* Unified modules into the 'configobj' package (#72, #31, #32)
* Added ``validate`` v1.1.0 shim to allow a gradual migration,
  rewrite your imports as ``from configobj.validate import …``
  to get rid of it
* Alternative line comment markers for more INI compatibility (#79)
* More detailed multi-error reports (#73)
* Added 'decoupled' mode to merge() (#115)
* fix: ``mixed_list`` accepts type name variants (#110)
* fix: Don't quote git-style section titles (#74)
* docs: Explicit mention of ``force_list`` and its pitfalls (#112)


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
