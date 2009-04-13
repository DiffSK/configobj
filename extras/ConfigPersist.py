# ConfigPersist.py
# Functions for using ConfigObj for data persistence
# Copyright (C) 2005 Michael Foord
# E-mail: fuzzyman AT voidspace DOT org DOT uk

# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/python/license.shtml

# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# For information about bugfixes, updates and support, please join the
# ConfigObj mailing list:
# http://lists.sourceforge.net/lists/listinfo/configobj-develop
# Comments, suggestions and bug reports welcome.

"""
Functions for doing data persistence with ConfigObj.

It requires access to the validate module and ConfigObj.
"""

__version__ = '0.1.0'

__all__ = (
    'add_configspec',
    'write_configspec',
    'add_typeinfo',
    'typeinfo_to_configspec',
    'vtor',
    'store',
    'restore',
    'save_configspec',
    '__version__'
    )

from configobj import ConfigObj

try:
    from validate import Validator
except ImportError:
    vtor = None
else:
    vtor = Validator()

def add_configspec(config):
    """
    A function that adds a configspec to a ConfigObj.
    
    Will only work for ConfigObj instances using basic datatypes :
    
        * floats
        * strings
        * ints
        * booleans
        * Lists of the above
    """
    config.configspec = {}
    for entry in config:
        val = config[entry]
        if isinstance(val, dict):
            # a subsection
            add_configspec(val)
        elif isinstance(val, bool):
            config.configspec[entry] = 'boolean'
        elif isinstance(val, int):
            config.configspec[entry] = 'integer'
        elif isinstance(val, float):
            config.configspec[entry] = 'float'
        elif isinstance(val, str):
            config.configspec[entry] = 'string'
        elif isinstance(val, (list, tuple)):
            list_type = None
            out_list = []
            for mem in val:
                if isinstance(mem, str):
                    this = 'string'
                elif isinstance(mem, bool):
                    this = 'boolean'
                elif isinstance(mem, int):
                    this = 'integer'
                elif isinstance(mem, float):
                    this = 'float'
                else:
                    raise TypeError('List member  "%s" is an innapropriate type.' % mem)
                if list_type and this != list_type:
                    list_type = 'mixed'
                elif list_type is None:
                    list_type = this
                out_list.append(this)
            if list_type is None:
                l = 'list(%s)'
            else:
                list_type = {'integer': 'int', 'boolean': 'bool',
                             'mixed': 'mixed', 'float': 'float',
                            'string': 'string' }[list_type]
                l = '%s_list(%%s)' % list_type
            config.configspec[entry] = l % str(out_list)[1:-1]
        #
        else:
            raise TypeError('Value "%s" is an innapropriate type.' % val)

def write_configspec(config):
    """Return the configspec (of a ConfigObj) as a list of lines."""
    out = []
    for entry in config:
        val = config[entry]
        if isinstance(val, dict):
            # a subsection
            m = config.main._write_marker('', val.depth, entry, '')
            out.append(m)
            out += write_configspec(val)
        else:
            name = config.main._quote(entry, multiline=False)
            out.append("%s = %s" % (name, config.configspec[entry]))
    #
    return out

def add_typeinfo(config):
    """
    Turns the configspec attribute of each section into a member of the
    section. (Called ``__types__``).
    
    You must have already called ``add_configspec`` on the ConfigObj.
    """
    for entry in config.sections:
        add_typeinfo(config[entry])
    config['__types__'] = config.configspec

def typeinfo_to_configspec(config):
    """Turns the '__types__' member of each section into a configspec."""
    for entry in config.sections:
        if entry == '__types__':
            continue
        typeinfo_to_configspec(config[entry])
    config.configspec = config['__types__']
    del config['__types__']

def store(config):
    """"
    Passed a ConfigObj instance add type info and save.
    
    Returns the result of calling ``config.write()``.
    """
    add_configspec(config)
    add_typeinfo(config)
    return config.write()

def restore(stored):
    """
    Restore a ConfigObj saved using the ``store`` function.
    
    Takes a filename or list of lines, returns the ConfigObj instance.
    
    Uses the built-in Validator instance of this module (vtor).
    
    Raises an ImportError if the validate module isn't available
    """
    if vtor is None:
        raise ImportError('Failed to import the validate module.')
    config = ConfigObj(stored)
    typeinfo_to_configspec(config)
    config.validate(vtor)
    return config

def save_configspec(config):
    """Creates a configspec and returns it as a list of lines."""
    add_configspec(config)
    return write_configspec(config)

def _test():
    """
    A dummy function for the sake of doctest.
    
    First test add_configspec
    >>> from configobj import ConfigObj
    >>> from validate import Validator
    >>> vtor = Validator()
    >>> config = ConfigObj()
    >>> config['member 1'] = 3
    >>> config['member 2'] = 3.0
    >>> config['member 3'] = True
    >>> config['member 4'] = [3, 3.0, True]
    >>> add_configspec(config)
    >>> assert config.configspec == { 'member 2': 'float',
    ...    'member 3': 'boolean', 'member 1': 'integer',
    ...    'member 4': "mixed_list('integer', 'float', 'boolean')"}
    >>> assert config.validate(vtor) == True
    
    Next test write_configspec - including a nested section
    >>> config['section 1'] = config.copy()
    >>> add_configspec(config)
    >>> a = config.write()
    >>> configspec = write_configspec(config)
    >>> b = ConfigObj(a, configspec=configspec)
    >>> assert b.validate(vtor) == True
    >>> assert b == config
    
    Next test add_typeinfo and typeinfo_to_configspec
    >>> orig = ConfigObj(config)
    >>> add_typeinfo(config)
    >>> a = ConfigObj(config.write())
    >>> typeinfo_to_configspec(a)
    >>> assert a.validate(vtor) == True
    >>> assert a == orig
    >>> typeinfo_to_configspec(config)
    >>> assert config.validate(vtor) == True
    >>> assert config == orig
    
    Test store and restore
    >>> a = store(config)
    >>> b = restore(a)
    >>> assert b == orig
    
    Test save_configspec
    >>> a = save_configspec(orig)
    >>> b = ConfigObj(b, configspec=a)
    >>> b.validate(vtor)
    1
    """

if __name__ == '__main__':
    # run the code tests in doctest format
    #
    import doctest
    doctest.testmod()

"""
ISSUES
======

TODO
====


CHANGELOG
=========

2005/09/07
----------

Module created.

"""