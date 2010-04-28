#!/usr/bin/env python
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
"""N queens problem
The problem is solved with a EnumeratorDistributor splitting
the smallest domain in at most N subdomains."""


from __future__ import generators

from logilab.constraint import *
from logilab.constraint.distributors import *
from chess import ChessDomain, QueensConstraint

def queens(size=8,verbose=0):
    variables = []
    domains = {}
    constraints = []
    for i in range(size):
        name = 'Q%02d'%i
        variables.append(name)
        domains[name] = ChessDomain(size)

    for q1 in variables:
        for q2 in variables:
            if q1 < q2:
                c = QueensConstraint((q1,q2))
                constraints.append(c)
    r = Repository(variables,domains,constraints)
    for sol in Solver(EnumeratorDistributor()).solve_all(r,verbose):
        yield sol



def draw_solution(s):
    size = len(s)
    queens = {}
    board = ''
    for q,p in s.items():
        queens[p]=q
    board += '_'*(size*2+1)+'\n'
    for i in range(size):
        #
        for j in range(size):
            q = queens.get((i,j))
            if q is None:
                board+='|'+'·-'[(i+j)%2]
            else:
                board+='|Q'
        board+='|\n'
    board += '¯'*(size*2+1)
    print board


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
    for sol in queens(size,verbose):
        count += 1
        if display:
            print 'solution #%d'%count
            draw_solution(sol)
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
