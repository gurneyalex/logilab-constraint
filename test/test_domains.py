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

class AbstractDomainTC(TestCase):
    """override the following methods:
     * setUp to initialize variables
     """
    def setUp(self):
        self.values = []
        self.domain = None
        raise NotImplementedError

    def testGetValues(self):
        """tests the getValues() method"""
        v1 = list(self.domain.getValues())
        v1.sort()
        v2 = self.values[:]
        v2.sort()
        self.assertEqual(v1, v2)

    def testSize(self):
        """tests the size() method"""
        self.assertEqual(self.domain.size(), len(self.values))
        self.domain.removeValue(self.values[0])
        self.assertEqual(self.domain.size(), len(self.values) - 1)

    def testRemove(self):
        """tests the removeValue() method"""
        self.domain.removeValue(self.values[0])
        self.assertNotIn(self.values[0], self.domain.getValues())

    def testEmptyDomain(self):
        """tests that a ConsistencyFailure exception is raised
        when the last value of a domain is removed"""
        exception = 0
        for v in self.values[1:]:
            self.domain.removeValue(v)
        try:
            self.domain.removeValue(self.values[0])
        except propagation.ConsistencyFailure:
            exception = 1
        self.assertTrue(exception)

class SuiteDomainTC(AbstractDomainTC):
    def setUp(self):
        self.values = list(range(3))
        self.domain = fd.FiniteDomain(self.values)



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
    import test_domains
    cases = cases or get_all_cases(test_domains)
    loader = unittest.defaultTestLoader
    loader.testMethodPrefix = 'test'
    loader.sortTestMethodsUsing = None # disable sorting
    suites = [loader.loadTestsFromTestCase(tc) for tc in cases]

    return TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest="suite")
