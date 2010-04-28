# pylint: disable-msg=W0232
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

"""Provides an psyobj class regardless of the availability of psyco"""

import os

try:
    if "NO_PSYCO" in os.environ:
        raise ImportError()
    from psyco.classes import psyobj as Psyobj # pylint: disable-msg=W0611
except ImportError:

    class Psyobj:
        pass

    if hasattr(os,'uname') and os.uname()[-1] == 'x86_64':
        pass # psyco only available for 32bits platforms
    else:
        from warnings import warn
        warn("Psyco could not be loaded."
             " Psyco is a Python just in time compiler available at http://psyco.sf.net"
             " Installing it will enhance the performance of logilab.constraint",
             stacklevel=2)


