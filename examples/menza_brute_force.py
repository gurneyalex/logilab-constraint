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
try:
    import psyco
    psyco.full()
except ImportError:
    print 'Psyco not available'

def menza():
    sol = []
    all_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for a in range(1000) :
        for b in range(100) :
            c = a*b
            if c > 9999:
                digits = list("%.3d%.2d%.5d" % (a, b, c))
                digits.sort()
                if digits == all_digits :
                    sol.append({'a': a, 'b': b})
                    print "%.3d x %.2d = %.5d" % (a, b, c)
    return sol

if __name__ == '__main__':
    sol = menza()
    print len(sol)
