.. _validate_doc:

---------------------------
 Using the Validator class
---------------------------


:Authors: Michael Foord, Nicola Larosa, Rob Dennis, Eli Courtwright, Mark Andrews
:Version: Validate 2.0.0
:Date: 2014/02/08
:Homepage: `Github Page`_
:License: `BSD License`_
:Support: `Mailing List`_

.. _Mailing List: http://lists.sourceforge.net/lists/listinfo/configobj-develop
.. _This Document:
.. _Github Page: https://github.com/DiffSK/configobj
.. _BSD License: http://opensource.org/licenses/BSD-3-Clause


.. contents:: Validate Manual


Introduction
============

Validation is used to check that supplied values conform to a specification.

The value can be supplied as a string, e.g. from a config file. In this case
the check will also *convert* the value to the required type. This allows you
to add validation as a transparent layer to access data stored as strings. The
validation checks that the data is correct *and* converts it to the expected
type.

Checks are also strings, and are easy to write. One generic system can be used
to validate information from different sources via a single consistent
mechanism.

Checks look like function calls, and map to function calls. They can include
parameters and keyword arguments. These arguments are passed to the relevant
function by the ``Validator`` instance, along with the value being checked.

The syntax for checks also allows for specifying a default value. This default
value can be ``None``, no matter what the type of the check. This can be used
to indicate that a value was missing, and so holds no useful value.

Functions either return a new value, or raise an exception. See `Validator
Exceptions`_ for the low down on the exception classes that ``validate.py``
defines.

Some standard functions are provided, for basic data types; these come built
into every validator. Additional checks are easy to write: they can be provided
when the ``Validator`` is instantiated, or added afterwards.

Validate was primarily written to support ConfigObj, but is designed to be
applicable to many other situations.

For support and bug reports please use the ConfigObj `Github Page`_


Downloading
===========

The current version is **2.0.0**, dated 8th February 2014.

You can obtain validate in the following ways :


Files
-----

* validate.py from `Github Page`_
* The latest development version can be obtained from the `Github Page`_.

The standard functions
======================

The standard functions come built-in to every ``Validator`` instance. They work
with the following basic data types :

* integer
* float
* boolean
* string
* ip_addr

plus lists of these datatypes.

Adding additional checks is done through coding simple functions.

The full set of standard checks are :

:'integer': matches integer values (including negative). Takes optional 'min'
            and 'max' arguments::

                integer()
                integer(3, 9)    # any value from 3 to 9
                integer(min=0) # any positive value
                integer(max=9)

:'float': matches float values
          Has the same parameters as the integer check.

:'boolean': matches boolean values: ``True`` or ``False``.
            Acceptable string values for True are::

             true, on, yes, 1

         Acceptable string values for False are::

             false, off, no, 0

         Any other value raises an error.

:'string': matches any string. Takes optional keyword args 'min' and 'max' to
           specify min and max length of string.

:'ip_addr': matches an Internet Protocol address, v.4, represented by a
            dotted-quad string, i.e. '1.2.3.4'.

:'list': matches any list. Takes optional keyword args 'min', and 'max' to
         specify min and max sizes of the list. The list checks always
         return a list.

:'force_list': is the same as 'list', but if anything but a list or tuple is passed in,
             it will coerce it into a list containing that value. Useful to avoid
             confusion for users not accustomed to Python idioms and thus forget the
             trailing comma to turn a single value into a list.

:'tuple': matches any list. This check returns a tuple rather than a list.

:'int_list': Matches a list of integers. Takes the same arguments as list.

:'float_list': Matches a list of floats. Takes the same arguments as list.

:'bool_list': Matches a list of boolean values. Takes the same arguments as
              list.

:'string_list': Matches a list of strings. Takes the same arguments as list.

:'ip_addr_list': Matches a list of IP addresses. Takes the same arguments as
                 list.

:'mixed_list': Matches a list with different types in specific positions.
               List size must match the number of arguments.

               Each position can be one of::

                   int, str, boolean, float, ip_addr

               So to specify a list with two strings followed by two integers,
               you write the check as::

                   mixed_list(str, str, int, int)

:'pass': matches everything: it never fails and the value is unchanged. It is
         also the default if no check is specified.

:'option': matches any from a list of options.
           You specify this test with::

               option('option 1', 'option 2', 'option 3')

The following code will work without you having to specifically add the
functions yourself.

.. code-block:: python

    from validate import Validator
    #
    vtor = Validator()
    newval1 = vtor.check('integer', value1)
    newval2 = vtor.check('boolean', value2)
    # etc ...

.. note::

    Of course, if these checks fail they raise exceptions. So you should wrap
    them in ``try...except`` blocks. Better still,  use ConfigObj for a higher
    level interface.


Using Validator
===============

Using ``Validator`` is very easy. It has one public attribute and one public
method.

Shown below are the different steps in using ``Validator``.

The only additional thing you need to know, is about `Writing check
functions`_.

Instantiate
-----------

.. code-block:: python

    from validate import Validator
    vtor = Validator()

or even :

.. code-block:: python

    from validate import Validator
    #
    fdict = {
        'check_name1': function1,
        'check_name2': function2,
        'check_name3': function3,
    }
    #
    vtor = Validator(fdict)


The second method adds a set of your functions as soon as your validator is
created. They are stored in the ``vtor.functions`` dictionary. The 'key' you
give them in this dictionary is the name you use in your checks (not the
original function name).

Dictionary keys/functions you pass in can override the built-in ones if you
want.


Adding functions
----------------

The code shown above, for adding functions on instantiation, has exactly the
same effect as the following code :

.. code-block:: python

    from validate import Validator
    #
    vtor = Validator()
    vtor.functions['check_name1'] = function1
    vtor.functions['check_name2'] = function2
    vtor.functions['check_name3'] = function3

``vtor.functions`` is just a dictionary that maps names to functions, so we
could also have called ``vtor.functions.update(fdict)``.


Writing the check
-----------------

As we've heard, the checks map to the names in the ``functions`` dictionary.
You've got a full list of `The standard functions`_ and the arguments they
take.

If you're using ``Validator`` from ConfigObj, then your checks will look like::

    keyword = int_list(max=6)

but the check part will be identical .


The check method
----------------

If you're not using ``Validator`` from ConfigObj, then you'll need to call the
``check`` method yourself.

If the check fails then it will raise an exception, so you'll want to trap
that. Here's the basic example :

.. code-block:: python

    from validate import Validator, ValidateError
    #
    vtor = Validator()
    check = "integer(0, 9)"
    value = 3
    try:
        newvalue = vtor.check(check, value)
    except ValidateError:
        print 'Check Failed.'
    else:
        print 'Check passed.'


.. caution::

    Although the value can be a string, if it represents a list it should
    already have been turned into a list of strings.


Default Values
~~~~~~~~~~~~~~

Some values may not be available, and you may want to be able to specify a
default as part of the check.

You do this by passing the keyword ``missing=True`` to the ``check`` method, as
well as a ``default=value`` in the check. (Constructing these checks is done
automatically by ConfigObj: you only need to know about the ``default=value``
part) :

.. code-block:: python

    check1 = 'integer(default=50)'
    check2 = 'option("val 1", "val 2", "val 3", default="val 1")'

    assert vtor.check(check1, '', missing=True) == 50
    assert vtor.check(check2, '', missing=True) == "val 1"


If you pass in ``missing=True`` to the check method, then the actual value is
ignored. If no default is specified in the check, a ``ValidateMissingValue``
exception is raised. If a default is specified then that is passed to the
check instead.

If the check has ``default=None`` (case sensitive) then ``vtor.check`` will
*always* return ``None`` (the object). This makes it easy to tell your program
that this check contains no useful value when missing, i.e. the value is
optional, and may be omitted without harm.


.. note::

    As of version 0.3.0, if you specify ``default='None'`` (note the quote marks
    around ``None``) then it will be interpreted as the string ``'None'``.


List Values
~~~~~~~~~~~

It's possible that you would like your default value to be a list. It's even
possible that you will write your own check functions - and would like to pass
them keyword arguments as lists from within the check.

To avoid confusing syntax with commas and quotes you use a list constructor to
specify that keyword arguments are lists. This includes the ``default`` value.
This makes checks look something like::

    checkname(default=list('val1', 'val2', 'val3'))


get_default_value
-----------------

``Validator`` instances have a ``get_default_value`` method. It takes a ``check`` string
(the same string you would pass to the ``check`` method) and returns the default value,
converted to the right type. If the check doesn't define a default value then this method
raises a ``KeyError``.

If the ``check`` has been seen before then it will have been parsed and cached already,
so this method is not expensive to call (however the conversion is done each time).



Validator Exceptions
====================

.. note::

    If you only use Validator through ConfigObj, it traps these Exceptions for
    you. You will still need to know about them for writing your own check
    functions.

``vtor.check`` indicates that the check has failed by raising an exception.
The appropriate error should be raised in the check function.

The base error class is ``ValidateError``. All errors (except for ``VdtParamError``)
raised are sub-classes of this.

If an unrecognised check is specified then ``VdtUnknownCheckError`` is
raised.

There are also ``VdtTypeError`` and ``VdtValueError``.

If incorrect parameters are passed to a check function then it will (or should)
raise ``VdtParamError``. As this indicates *programmer* error, rather than an error
in the value, it is a subclass of ``SyntaxError`` instead of ``ValidateError``.

.. note::

    This means it *won't* be caught by ConfigObj - but propagated instead.

If the value supplied is the wrong type, then the check should raise
``VdtTypeError``. e.g. the check requires the value to be an integer (or
representation of an integer) and something else was supplied.

If the value supplied is the right type, but an unacceptable value, then the
check should raise ``VdtValueError``. e.g. the check requires the value to
be an integer (or representation of an integer) less than ten and a higher
value was supplied.

Both ``VdtTypeError`` and ``VdtValueError`` are initialised with the
incorrect value. In other words you raise them like this :

.. code-block:: python

    raise VdtTypeError(value)
    #
    raise VdtValueError(value)


``VdtValueError`` has the following subclasses, which should be raised if
they are more appropriate.

* ``VdtValueTooSmallError``
* ``VdtValueTooBigError``
* ``VdtValueTooShortError``
* ``VdtValueTooLongError``


Writing check functions
=======================

Writing check functions is easy.

The check function will receive the value as its first argument, followed by
any other parameters and keyword arguments.

If the check fails, it should raise a ``VdtTypeError`` or a
``VdtValueError`` (or an appropriate subclass).

All parameters and keyword arguments are *always* passed as strings. (Parsed
from the check string).

The value might be a string (or list of strings) and need
converting to the right type - alternatively it might already be a list of
integers. Our function needs to be able to handle either.

If the check passes then it should return the value (possibly converted to the
right type).

And that's it !


Example
-------

Here is an example function that requires a list of integers. Each integer
must be between 0 and 99.

It takes a single argument specifying the length of the list. (Which allows us
to use the same check in more than one place). If the length can't be converted
to an integer then we need to raise ``VdtParamError``.

Next we check that the value is a list. Anything else should raise a
``VdtTypeError``. The list should also have 'length' entries. If the list
has more or less entries then we will need to raise a
``VdtValueTooShortError`` or a ``VdtValueTooLongError``.

Then we need to check every entry in the list. Each entry should be an integer
between 0 and 99, or a string representation of an integer between 0 and 99.
Any other type is a ``VdtTypeError``, any other value is a
``VdtValueError`` (either too big, or too small).

.. code-block:: python

    def special_list(value, length):
        """
        Check that the supplied value is a list of integers,
        with 'length' entries, and each entry between 0 and 99.
        """
        # length is supplied as a string
        # we need to convert it to an integer
        try:
            length = int(length)
        except ValueError:
            raise VdtParamError('length', length)
        #
        # Check the supplied value is a list
        if not isinstance(value, list):
            raise VdtTypeError(value)
        #
        # check the length of the list is correct
        if len(value) > length:
            raise VdtValueTooLongError(value)
        elif len(value) < length:
            raise VdtValueTooShortError(value)
        #
        # Next, check every member in the list
        # converting strings as necessary
        out = []
        for entry in value:
            if not isinstance(entry, (str, unicode, int)):
                # a value in the list
                # is neither an integer nor a string
                raise VdtTypeError(value)
            elif isinstance(entry, (str, unicode)):
                if not entry.isdigit():
                    raise VdtTypeError(value)
                else:
                    entry = int(entry)
            if entry < 0:
                raise VdtValueTooSmallError(value)
            elif entry > 99:
                raise VdtValueTooBigError(value)
            out.append(entry)
        #
        # if we got this far, all is well
        # return the new list
        return out

If you are only using validate from ConfigObj then the error type (*TooBig*,
*TooSmall*, etc) is lost - so you may only want to raise ``VdtValueError``.

.. caution::

    If your function raises an exception that isn't a subclass of
    ``ValidateError``, then ConfigObj won't trap it. This means validation will
    fail.

    This is why our function starts by checking the type of the value. If we
    are passed the wrong type (e.g. an integer rather than a list) we get a
    ``VdtTypeError`` rather than bombing out when we try to iterate over
    the value.

If you are using validate in another circumstance you may want to create your
own subclasses of ``ValidateError`` which convey more specific information.


Known Issues
============

The following parses and then blows up. The resulting error message
is confusing:

    ``checkname(default=list(1, 2, 3, 4)``

This is because it parses as: ``checkname(default="list(1", 2, 3, 4)``.
That isn't actually unreasonable, but the error message won't help you
work out what has happened.


TODO
====

* A regex check function ?
* A timestamp check function ? (Using the ``parse`` function from ``DateUtil`` perhaps).


ISSUES
======

.. note::

    Please file any bug reports to the `Github Page`_

If we could pull tuples out of arguments, it would be easier
to specify arguments for 'mixed_lists'.


CHANGELOG
=========

2014/02/08 - Version 2.0.0
--------------------------
* Python 3 single-source compatibility at the cost of a more restrictive set of versions: 2.6, 2.7, 3.2, 3.3 (otherwise unchanged)
* New maintainers: Rob Dennis and Eli Courtwright
* New home on github

2009/10/25 - Version 1.0.1
--------------------------

* BUGFIX: Fixed compatibility with Python 2.3.

2009/04/13 - Version 1.0.0
--------------------------

* BUGFIX: can now handle multiline strings.
* Addition of 'force_list' validation option.

As the API is stable and there are no known bugs or outstanding feature requests I am marking this 1.0.


2008/02/24 - Version 0.3.2
--------------------------

BUGFIX: Handling of None as default value fixed.


2008/02/05 - Version 0.3.1
--------------------------

BUGFIX: Unicode checks no longer broken.


2008/02/05 - Version 0.3.0
--------------------------

Improved performance with a parse cache.

New ``get_default_value`` method. Given a check it returns the default
value (converted to the correct type) or raises a ``KeyError`` if the
check doesn't specify a default.

Added 'tuple' check and corresponding 'is_tuple' function (which always returns a tuple).

BUGFIX: A quoted 'None' as a default value is no longer treated as None,
but as the string 'None'.

BUGFIX: We weren't unquoting keyword arguments of length two, so an
empty string didn't work as a default.

BUGFIX: Strings no longer pass the 'is_list' check. Additionally, the
list checks always return lists.

A couple of documentation bug fixes.

Removed CHANGELOG from module.


2007/02/04      Version 0.2.3
-----------------------------

Release of 0.2.3


2006/12/17      Version 0.2.3-alpha1
------------------------------------

By Nicola Larosa

Fixed validate doc to talk of ``boolean`` instead of ``bool``; changed the
``is_bool`` function to ``is_boolean`` (Sourceforge bug #1531525).


2006/04/29      Version 0.2.2
-----------------------------

Addressed bug where a string would pass the ``is_list`` test. (Thanks to
Konrad Wojas.)


2005/12/16      Version 0.2.1
-----------------------------

Fixed bug so we can handle keyword argument values with commas.

We now use a list constructor for passing list values to keyword arguments
(including ``default``)::

    default=list("val", "val", "val")

Added the ``_test`` test.

Moved a function call outside a try...except block.


2005/08/18      Version 0.2.0
-----------------------------

Updated by Michael Foord and Nicola Larosa

Does type conversion as well.


2005/02/01      Version 0.1.0
-----------------------------

Initial version developed by Michael Foord and Mark Andrews.
