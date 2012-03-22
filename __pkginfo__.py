# pylint: disable-msg=W0622
# copyright 2002-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

numversion = (0, 4, 1)
version = '.'.join(map(str, numversion))
pyversions = ('2.4','2.5', '2.6')

license = 'LGPL'
copyright = '''Copyright (c) 2002-2010 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr'''

short_desc = "constraints satisfaction solver in Python"

long_desc = """Extensible constraint satisfaction problem solver written in pure
Python, using constraint propagation algorithms. The
logilab.constraint module provides finite domains with arbitrary
values, finite interval domains, and constraints which can be applied
to variables linked to these domains.
"""

author = "Alexandre Fayolle"
author_email = "alexandre.fayolle@logilab.fr"

web = "http://www.logilab.org/projects/%s" % modname
ftp = "ftp://ftp.logilab.org/pub/%s/" % modname
mailinglist = "http://lists.logilab.org/mailman/listinfo/python-logic/"

subpackage_of = 'logilab'
debian_name = 'constraint'
debian_maintainer_email = 'afayolle@debian.org'
