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
"""
Solve a puzzle that got discussed on c.l.p. on october 2002

ABC*DE=FGHIJ with all letters different and in domain [0,9]
"""
from __future__ import generators

from logilab.constraint import *
from logilab.constraint.distributors import DichotomyDistributor
from logilab.constraint.propagation import BasicConstraint, ConsistencyFailure

class DistinctDigits(BasicConstraint):
    def __init__(self,variable):
        BasicConstraint.__init__(self,variable,None,None)

    def narrow(self,domains):
        domain = domains[self._variable]
        try:
            for v in domain.getValues():
                s = str(v)
                for d in ('0','1','2','3','4','5','6','7','8','9'):
                    if s.count(d) not in (0,1):
                        domain.removeValue(v)
                        break
        except ConsistencyFailure, e:
            raise ConsistencyFailure('inconsistency while applying %s'%repr(self))
        return 1
        
    def __repr__(self):
        return '<DistinctDigits>'


    
def mensa() :
    """
    ABC*DE=FGHIJ with all letters different and in domain [0,9]
    """

    VARS='xy'
    variables = list(VARS)
    domains = {}
    constraints = []

    # x = ABC and y = DE, x*y = FGHIJ
    domains['x'] = fd.FiniteDomain(range(0,1000))
    domains['y'] = fd.FiniteDomain(range(0,100))
    
    # x and y *must* have distinct digits themselves
    # (for example this will remove 232 from x's domain)
    for v in variables:
        constraints.append(DistinctDigits(v))

    # x,y and x*y must have distinct digits
    dist = []
    for digit in range(10):
        dist.append('("%%.3d%%.2d%%.5d" %% (x,y,x*y)).count("%d")==1'%digit)
    c = ' and '.join(dist)
    constraints.append(fd.make_expression(('x','y'),c))
    r = Repository(variables, domains, constraints)
    return r

if __name__ == '__main__' :
    import sys,getopt
    opts,args = getopt.getopt(sys.argv[1:],'dv')
    verbose = 0
    display = 0
    for o,v in opts:
        if o == '-v':
            verbose += 1
        elif o == '-d':
            display = 1

    r = mensa()
    print 'problem created. let us solve it.'
    s = []
    for sol in Solver().solve_all(r,verbose):
        s.append(sol)
        if display:
            sol['c'] = sol['x']*sol['y']
            print "%(x)s x %(y)s = %(c)s" % sol
    if not display:
        print 'Found %d solutions'%len(s)
