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
from logilab.constraint.propagation import BasicConstraint, ConsistencyFailure

class DistinctDigits(BasicConstraint):
    def __init__(self,variable):
        BasicConstraint.__init__(self,variable,None,None)

    def narrow(self,domains):
        domain = domains[self._variable]
        for v in domain.getValues():
            s = str(v)
            for d in ('0','1','2','3','4','5','6','7','8','9'):
                if s.count(d) not in (0,1):
                    domain.removeValue(v)
                    break
        return 1

    def __repr__(self):

        return '<DistinctDigits on variable %s>'%self._variable


def menza() :
    """
    """

    VARS='ab'
    variables = list(VARS)
    domains = {}
    constraints = []

    domains['a'] = fd.FiniteDomain(range(0,1000))
    domains['b'] = fd.FiniteDomain(range(0,100))

    me = fd.make_expression

    for v in variables:
        constraints.append(DistinctDigits(v))
    dist = ['10000 < a*b ']
    for digit in range(10):
        dist.append('("%%.3d%%.2d%%.5d" %% (a,b,a*b)).count("%d")==1'%digit)
    constraints.append(me(('a','b'),' and '.join(dist)))
    r = Repository(variables, domains, constraints)
    return r

if __name__ == '__main__' :
    import sys,getopt
    opts,args = getopt.getopt(sys.argv[1:],'dv')
    verbose = 0
    display = 0
    create_problem=menza
    for o,v in opts:
        if o == '-v':
            verbose += 1
        elif o == '-d':
            display = 1


    r = create_problem()
    print 'problem created. let us solve it.'
    s = []
    for sol in Solver().solve_all(r,verbose):
        s.append(sol)
        if display:
            sol['c'] = sol['a']*sol['b']
            print "%(a)s x %(b)s = %(c)s" % sol
    if not display:
        print 'Found %d solutions'%len(s)
