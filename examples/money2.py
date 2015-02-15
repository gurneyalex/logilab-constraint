#!/usr/bin/env python2.2
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

from __future__ import print_function

from logilab.constraint import *
from logilab.constraint.distributors import SplitDistributor

def money(verbose=0):
    """ SEND
       +MORE
      -------
       MONEY
    """
    digits = range(10)
    variables = list('sendmory')
    domains = {}
    constraints = []
    for v in variables:
        domains[v] = fd.FiniteDomain(digits)

    constraints.append(fd.AllDistinct(variables))
    constraints.append(fd.NotEquals('m', 0))
    constraints.append(fd.NotEquals('s', 0))
    for v1 in variables:
        for v2 in variables:
            if v1 < v2:
                constraints.append(fd.make_expression((v1, v2),
                                                      '%s != %s'%(v1, v2)))
    constraints.append(fd.make_expression(variables,
                'm*10000+(o-m-s)*1000+(n-o-e)*100+(e-r-n)*10+y-e-d == 0'))
    r = Repository(variables, domains, constraints)
    s = Solver(distributor=SplitDistributor(10)).solve_one(r, verbose)
    return s

def display_solution(d):
    print('  SEND\t  \t','  %(s)d%(e)d%(n)d%(d)d'%d)
    print('+ MORE\t  \t','+ %(m)d%(o)d%(r)d%(e)d'%d)
    print('------\t-->\t','------')
    print(' MONEY\t  \t',' %(m)d%(o)d%(n)d%(e)d%(y)d'%d)

if __name__ == '__main__':
    print('WARNING!')
    print('This example takes looooooooooooooots of CPU to complete.')
    print('try money.py for a faster version.')
    import sys, getopt
    opts, args = getopt.getopt(sys.argv[1:], 'dv')
    verbose = 0
    display = 0
    for o,v in opts:
        if o == '-v':
            verbose += 1
        if o == '-d':
            display = 1
    sol = money(verbose)
    if display:
        display_solution(sol)
    else:
        print(sol)
