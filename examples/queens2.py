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

from __future__ import print_function

from logilab.constraint import *
from logilab.constraint.distributors import *

distributors = {
    "enum" : EnumeratorDistributor,
    "dicho" : DichotomyDistributor,
    "naive" : NaiveDistributor,
    "random" : RandomizingDistributor,
    }

def queens(size=8,verbose=0,distrib="enum"):
    variables = []
    domains = {}
    constraints = []
    for i in range(size):
        name = 'Q%02d'%i
        variables.append(name)
        domains[name] = fd.FiniteDomain( range(size) )

    for r1 in range(size):
        q1 = 'Q%02d' % r1
        for r2 in range(r1+1, size):
            q2 = 'Q%02d' % r2
            D = {'q1':q1,'q2':q2, 'diag':(r2-r1) }
            c = fd.make_expression((q1,q2),
                                   '%(q1)s != %(q2)s and '
                                   '%(diag)s != abs(%(q1)s-%(q2)s)'% D )
            constraints.append(c)

    r = Repository(variables,domains,constraints)
    Distrib = distributors[distrib]
    for sol in Solver(Distrib()).solve_all(r,verbose):
        yield sol



def draw_solution(s):
    size = len(s)
    board = ''
    queens = s.items()
    queens.sort()
    board += '_'*(size*2+1)+'\n'
    for i in range(size):
        qj = queens[i][1]
        for j in range(size):
            if j != qj:
                board+='|'+'�-'[(i+j)%2]
            else:
                board+='|Q'
        board+='|\n'
    board += '�'*(size*2+1)
    print(board)


def main(args = None):
    import sys,getopt
    if args is None:
        args = sys.argv[1:]
    opts,args = getopt.getopt(args,'dvfD:')
    display = 0
    verbose = 0
    first = 0
    distrib = "enum"
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
        elif o == "-D":
            if v in distributors:
                distrib = v
            else:
                raise RuntimeError("Distributor must be one of %s" % ", ".join(distributors.keys()) )
    count = 0
    for sol in queens(size,verbose,distrib):
        count += 1
        if display:
            print('solution #%d'%count)
            draw_solution(sol)
            print('*'*80)
        if first:
            break
    if not display:
        print('Use -d option to display solutions')
    print(count,'solutions found.')

    print("Domains copy:", fd.FiniteDomain._copy_count)
    print("Domains writes:", fd.FiniteDomain._write_count)

if __name__ == '__main__':
##     import hotshot
##     p = hotshot.Profile('/tmp/queens.prof')
##     p.runcall(main)
##     p.close()
    main()
