# pylint: disable-msg=W0622
# copyright 2002-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-constraint.
#
# logilab-constraint is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-constraint is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-constraint. If not, see <http://www.gnu.org/licenses/>.

modname = 'constraint'
distname = 'logilab-constraint'

numversion = (0, 6, 0)
version = '.'.join(map(str, numversion))

license = 'LGPL'
copyright = '''Copyright (c) 2002-2010 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr'''

description = "constraints satisfaction solver in Python"

long_desc = """Extensible constraint satisfaction problem solver written in pure
Python, using constraint propagation algorithms. The
logilab.constraint module provides finite domains with arbitrary
values, finite interval domains, and constraints which can be applied
to variables linked to these domains.
"""

author = "Alexandre Fayolle"
author_email = "contact@logilab.fr"

web = "http://www.logilab.org/projects/%s" % distname
mailinglist = "http://lists.logilab.org/mailman/listinfo/python-logic/"

subpackage_of = 'logilab'

classifiers = ["Topic :: Scientific/Engineering",
               "Programming Language :: Python",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 3",
               ]

install_requires = ['setuptools',
                    'logilab-common >= 0.63.2',
                    'six >= 1.4.0']
tests_require = []
