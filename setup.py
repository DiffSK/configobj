# setup.py
# Install script for ConfigObj
# Copyright (C) 2005 Michael Foord, Mark Andrews, Nicola Larosa
# E-mail: fuzzyman AT voidspace DOT org DOT uk
#         mark AT la-la DOT com
#         nico AT tekNico DOT net

# This software is licensed under the terms of the BSD license.
# http://www.voidspace.org.uk/python/license.shtml
# Basically you're free to copy, modify, distribute and relicense it,
# So long as you keep a copy of the license with it.

# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# For information about bugfixes, updates and support, please join the
# Rest2Web mailing list:
# http://lists.sourceforge.net/lists/listinfo/rest2web-develop
# Comments, suggestions and bug reports welcome.
"""
**setup.py** for ``configobj`` and ``validate`` modules.
"""

if __name__ == '__main__':
    import sys
    from distutils.core import setup
    from configobj import __version__ as VERSION

    NAME = 'configobj'
    MODULES = 'configobj', 'validate'
    DESCRIPTION = 'Config file reading, writing, and validation.'
    URL = 'http://www.voidspace.org.uk/python/configobj.html'
    LICENSE = 'BSD'
    PLATFORMS = ["Platform Independent"]

    if sys.version < '2.2.3':
        from distutils.dist import DistributionMetadata
        DistributionMetadata.classifiers = None
        DistributionMetadata.download_url = None

    setup(name= NAME,
          version= VERSION,
          description= DESCRIPTION,
          license = LICENSE,
          platforms = PLATFORMS,
          author= 'Michael Foord & Nicola Larosa',
          author_email= 'fuzzyman@voidspace.org.uk',
          url= URL,
          py_modules = MODULES,
         )
