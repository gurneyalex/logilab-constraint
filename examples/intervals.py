#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
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
Example problem with intervals
"""


from logilab.constraint import *
from logilab.constraint.distributors import *

def intervals(size=5,verbose=0):
    variables = []
    domains = {}
    constraints = []
    for i in range(size):
        name = 'v%02d'%i
        variables.append(name)
        domains[name] = fi.FiniteIntervalDomain(0, size*5, 5)

    for i, q1 in enumerate(variables):
        if i+1 == len(variables):
            continue
        q2 = variables[i+1]
        c = fi.StartsAfterEnd(q1, q2)
        constraints.append(c)

##     print domains
##     print constraints
    r = Repository(variables,domains,constraints)
    for sol in Solver(fi.FiniteIntervalDistributor()).solve_all(r,verbose):
        yield sol

def main(args = None):
    import sys,getopt
    if args is None:
        args = sys.argv[1:]
    opts,args = getopt.getopt(args,'dvf')
    display = 0
    verbose = 0
    first = 0
    if args:
        size = int(args[0])
    else:
        size = 8
    for o,v in opts:
        if o == '-d':
            display = 1
        elif o == '-v':
            verbose += 1
        elif o == "-f":
            first = 1
    count = 0
    for sol in intervals(size,verbose):
        count += 1
        if display:
            print sol
            print '*'*80
        if first:
            break
    if not display:
        print 'Use -d option to display solutions'
    print count,'solutions found.'

if __name__ == '__main__':
##     import hotshot
##     p = hotshot.Profile('/tmp/queens.prof')
##     p.runcall(main)
##     p.close()
    main()
