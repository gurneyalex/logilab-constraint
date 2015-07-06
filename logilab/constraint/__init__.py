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
"""Constraint Satisfaction Problem (CSP) Solver in Python."""

import pkg_resources

from logilab.constraint.propagation import Repository, Solver
from logilab.constraint.distributors import DefaultDistributor
from logilab.constraint import fd
from logilab.constraint import fi

__all__ = ['Repository', 'Solver', 'DefaultDistributor', 'fd', 'fi']
__version__ = pkg_resources.get_distribution('logilab-constraint').version
