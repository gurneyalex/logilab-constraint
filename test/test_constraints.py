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
"""Unit testing for constraint propagation module"""

import unittest

from six.moves import range
from logilab.common.testlib import TestCase, TestSuite

from logilab.constraint import fd
from logilab.constraint import propagation
from logilab.constraint import distributors


class AbstractConstraintTC(TestCase):
    """override the following methods:
     * setUp to initialize variables
     * narrowingAssertions to check that narrowing was ok
     """
    def setUp(self):
        self.relevant_variables = []
        self.irrelevant_variable = 'tagada'
        self.constraint = None #AbstractConstraint(self.relevant_variables)
        self.domains = {}
        self.entailed_domains = {}
        #raise NotImplementedError

    def testRelevance(self):
        """tests that relevant variables are relevant"""
        for v in self.relevant_variables:
            self.assertTrue(self.constraint.isVariableRelevant(v))
        self.failIf(self.constraint.isVariableRelevant(self.irrelevant_variable))


    def testNarrowing(self):
        """tests that narrowing is performed correctly"""
        entailed = self.constraint.narrow(self.domains)
        self.narrowingAssertions()

    def testEntailment(self):
        """tests that narrowing is performed correctly"""
        entailed = self.constraint.narrow(self.entailed_domains)
        self.assertTrue(entailed)

class AllDistinctTC(AbstractConstraintTC):
    def setUp(self):
        self.relevant_variables = ['x','y','z']
        self.irrelevant_variable = 'tagada'
        self.constraint = fd.AllDistinct(self.relevant_variables)
        self.domains = {'x':fd.FiniteDomain((1,2)),
                        'y':fd.FiniteDomain((1,3)),
                        'z':fd.FiniteDomain((1,4)),}

        self.entailed_domains = {'x':fd.FiniteDomain((1,)),
                                 'y':fd.FiniteDomain((1,2)),
                                 'z':fd.FiniteDomain((1,2,3)),}

    def narrowingAssertions(self):
        vx = self.domains['x'].getValues()
        vy = self.domains['y'].getValues()
        vz = self.domains['z'].getValues()
        self.assertIn(1, vx)
        self.assertIn(2, vx)
        self.assertIn(1, vy)
        self.assertIn(3, vy)
        self.assertIn(1, vz)
        self.assertIn(4, vz)

    def testNarrowing2(self):
        domains = {'x':fd.FiniteDomain((1,2)),
                   'y':fd.FiniteDomain((1,)),
                   'z':fd.FiniteDomain((1,4)),}
        entailed = self.constraint.narrow(domains)
        vx = domains['x'].getValues()
        vy = domains['y'].getValues()
        vz = domains['z'].getValues()
        self.assertTrue(entailed)
        self.assertIn(2, vx)
        self.assertIn(1, vy)
        self.assertIn(4, vz)

    def testNarrowing3(self):
        domains = {'x':fd.FiniteDomain((1,)),
                   'y':fd.FiniteDomain((2,)),
                   'z':fd.FiniteDomain((1,2,3,4)),}
        entailed = self.constraint.narrow(domains)
        vx = domains['x'].getValues()
        vy = domains['y'].getValues()
        vz = domains['z'].getValues()
        self.assertFalse(entailed)
        self.assertIn(1, vx)
        self.assertIn(2, vy)
        self.assertIn(4, vz)
        self.assertIn(3, vz)

    def testNarrowing4(self):
        domains = {'x':fd.FiniteDomain((1,)),
                   'y':fd.FiniteDomain((2,)),
                   'z':fd.FiniteDomain((1,3,4)),
                   't':fd.FiniteDomain((2,5,4)),
                   'u':fd.FiniteDomain((1,2,4)),
                   }
        constraint = fd.AllDistinct(domains.keys())
        entailed = constraint.narrow(domains)
        vx = domains['x'].getValues()
        vy = domains['y'].getValues()
        vz = domains['z'].getValues()
        vt = domains['t'].getValues()
        vu = domains['u'].getValues()
        self.failUnless(entailed)
        self.assertEqual([1],  vx)
        self.assertEqual([2], vy)
        self.assertEqual([3], vz)
        self.assertEqual([5], vt)
        self.assertEqual([4], vu)

    def testFailure1(self):
        domains = {'x':fd.FiniteDomain((1,2)),
                   'y':fd.FiniteDomain((2,1)),
                   'z':fd.FiniteDomain((1,2)),}
        exception = 0
        try:
            entailed = self.constraint.narrow(domains)
        except propagation.ConsistencyFailure:
            exception = 1
        self.assertTrue(exception)

    def testFailure2(self):
        domains = {'x':fd.FiniteDomain((1,)),
                   'y':fd.FiniteDomain((2,)),
                   'z':fd.FiniteDomain((1,2)),}
        exception = 0
        try:
            entailed = self.constraint.narrow(domains)
        except propagation.ConsistencyFailure:
            exception = 1
        self.assertTrue(exception)

    def testFailure3(self):
        domains = {'x':fd.FiniteDomain((1,)),
                   'y':fd.FiniteDomain((1,)),
                   'z':fd.FiniteDomain((2,3)),}
        exception = 0
        try:
            entailed = self.constraint.narrow(domains)
        except propagation.ConsistencyFailure:
            exception = 1
        self.assertTrue(exception)



class UnaryMathConstrTC(AbstractConstraintTC):
    def setUp(self):
        self.relevant_variables = ['x']
        self.irrelevant_variable = 'tagada'
        self.constraint = fd.make_expression(self.relevant_variables,
                                             'x==2')
        self.domains = {'x':fd.FiniteDomain(range(4))}
        self.entailed_domains = {'x':fd.FiniteDomain([2])}
    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [2])

class BinaryMathConstrTC(AbstractConstraintTC):
    def setUp(self):
        self.relevant_variables = ['x','y']
        self.irrelevant_variable = 'tagada'
        self.constraint = fd.make_expression(self.relevant_variables,
                                             'x+y==2')
        self.domains = {'x':fd.FiniteDomain(range(4)),
                        'y':fd.FiniteDomain(range(2))}
        self.entailed_domains = {'x':fd.FiniteDomain([2]),
                                 'y':fd.FiniteDomain([0])}
    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [1,2])
        v = list(self.domains['y'].getValues())
        v.sort()
        self.assertEqual(v, [0,1])

class TernaryMathConstrTC(AbstractConstraintTC):
    def setUp(self):
        self.relevant_variables = ['x','y','z']
        self.irrelevant_variable = 'tagada'
        self.constraint = fd.make_expression(self.relevant_variables,
                                             'x+y==2 and z>1')
        self.domains = {'x':fd.FiniteDomain(range(4)),
                        'y':fd.FiniteDomain(range(3)),
                        'z':fd.FiniteDomain(range(4))}
        self.entailed_domains = {'x':fd.FiniteDomain([2]),
                                 'y':fd.FiniteDomain([0]),
                                 'z':fd.FiniteDomain([2,3]),}


    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [0,1,2])
        v = list(self.domains['y'].getValues())
        v.sort()
        self.assertEqual(v, [0,1,2])
        v = list(self.domains['z'].getValues())
        v.sort()
        self.assertEqual(v, [2,3])

class AbstractBasicConstraintTC(TestCase):
    """override the following methods:
     * setUp to initialize variables
     * narrowingAssertions to check that narrowing was ok
     """
    def setUp(self):
        self.constraint = None #AbstractConstraint(self.relevant_variables)
        self.domains = {}
        self.entailed_domains = {}
        #raise NotImplementedError

    def testRelevance(self):
        """tests that relevant variables are relevant"""
        self.assertTrue(self.constraint.isVariableRelevant('x'))
        self.assertFalse(self.constraint.isVariableRelevant('tagada'))

    def testGetVariable(self):
        """test that getVariable returns the right variable"""
        self.assertEqual(self.constraint.getVariable(), 'x')

    def testNarrowing(self):
        """tests that narrowing is performed correctly"""
        entailed = self.constraint.narrow(self.domains)
        self.narrowingAssertions()

    def testEntailment(self):
        """tests that narrowing is performed correctly"""
        entailed = self.constraint.narrow(self.domains)
        self.assertTrue(entailed)


class EqualsConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.Equals('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [1])

class NotEqualsConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.NotEquals('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [0,2])

class LesserThanConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.LesserThan('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [0])

class LesserOrEqualConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.LesserOrEqual('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [0,1])

class GreaterThanConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.GreaterThan('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [2])

class GreaterOrEqualConstrTC(AbstractBasicConstraintTC):
    def setUp(self):
        self.constraint = fd.GreaterOrEqual('x',1)
        self.domains = {'x':fd.FiniteDomain(range(3))}

    def narrowingAssertions(self):
        v = list(self.domains['x'].getValues())
        v.sort()
        self.assertEqual(v, [1,2])


def get_all_cases(module):
    from inspect import isclass
    all_cases = []
    for name in dir(module):
        obj = getattr(module, name)
        if isclass(obj) and issubclass(obj, TestCase) and \
               not name.startswith('Abstract'):
            all_cases.append(obj)
    all_cases.sort(key=lambda x: x.__name__)
    return all_cases

def suite(cases = None):
    import test_constraints
    cases = cases or get_all_cases(test_constraints)
    loader = unittest.defaultTestLoader
    loader.testMethodPrefix = 'test'
    loader.sortTestMethodsUsing = None # disable sorting
    suites = [loader.loadTestsFromTestCase(tc) for tc in cases]

    return TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest="suite")
