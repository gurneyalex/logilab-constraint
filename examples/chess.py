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
"""Chess constraints and domains"""


from logilab.constraint import fd
from logilab.constraint.propagation import AbstractConstraint, ConsistencyFailure

class ChessDomain(fd.FiniteDomain):
    def __init__(self, size):
        values = [(i,j) for i in range(size) for j in range(size)]
        fd.FiniteDomain.__init__(self, values)

    def __repr__(self):
        vals = self.getValues()
        vals.sort()
        return '<ChessDomain %s>' % str(vals)

class QueensConstraint(AbstractConstraint):
    def __init__(self, variables):
        AbstractConstraint.__init__(self, variables)

    def __repr__(self):
        return '<QueensConstraint %s>' % str(self._variables)

    def narrow(self, domains):
        maybe_entailed = 1
        var1 = self._variables[0]
        dom1 = domains[var1]
        values1 = dom1.getValues()
        var2 = self._variables[1]
        dom2 = domains[var2]
        values2 = dom2.getValues()

        keep1 = {}
        keep2 = {}
        maybe_entailed = 1
        for val1 in values1:
            val1_0 = val1[0]
            val1_1 = val1[1]
            for val2 in values2:
                if val1 in keep1 and val2 in keep2 and maybe_entailed == 0:
                    continue
                val2_0 = val2[0]
                val2_1 = val2[1]
                if val1_0  < val2_0 and \
                   val1_1 != val2_1 and \
                   abs(val1_0-val2_0) != abs(val1_1-val2_1):
                    keep1[val1] = 1
                    keep2[val2] = 1
                else:
                    maybe_entailed = 0

        try:
            dom1.removeValues([val for val in values1 if val not in keep1])
            dom2.removeValues([val for val in values2 if val not in keep2])
        except ConsistencyFailure:
            raise ConsistencyFailure('Inconsistency while applying %s' % \
                                     repr(self))
        except Exception:
            print self, kwargs
            raise
        return maybe_entailed

