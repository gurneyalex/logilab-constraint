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
from logilab.common.testlib import TestCase, TestSuite
from logilab.constraint import distributors,fd


class AbstractDistributorTC(TestCase):
    """override the following methods:
     * buildDistributor to create the distributor
     * distributionAssertions to check that distribution was OK
     """
    def setUp(self):
        self.variables = ('v1','v2','v3')
        self.domains1 = {'v1':fd.FiniteDomain([1]),
                        'v2':fd.FiniteDomain([2,3]),
                        'v3':fd.FiniteDomain([4,5,6,7]),
                         }
        self.domains2 = {'v1':fd.FiniteDomain([1]),
                        'v2':fd.FiniteDomain([2,3,4,5,6]),
                        'v3':fd.FiniteDomain([7,8,9,10,11,12,13]),
                         }
        self.distributor = self.buildDistributor()
        
    def buildDistributor(self):
        """returns a distributor"""
        raise NotImplementedError
    
    def distributionAssertions(self):
        """checks the distribution"""
        raise NotImplementedError

    def testFindSmallestDomain(self):
        """tests that the smallest domain is indeed the smallest one
        with at least 2 values inside"""
        dist = self.buildDistributor()
        self.assertEquals('v2', dist.findSmallestDomain(self.domains1))
        self.assertEquals('v2', dist.findSmallestDomain(self.domains2))

    def testFindLargestDomain(self):
        """tests that the largest domain is indeed the largest one"""
        dist = self.buildDistributor()
        self.assertEquals('v3', dist.findLargestDomain(self.domains1))
        self.assertEquals('v3', dist.findLargestDomain(self.domains2))

    def testSingleValueDomainNotDistributed(self):
        """tests that a domain of size 1 is not distributed"""
        for initial_domain in (self.domains1,self.domains2):
            distributed_domains = self.distributor.distribute(self.domains1)
            for d in distributed_domains:
                assert d['v1'].size() == initial_domain['v1'].size()
    

    def testDistribution(self):
        """tests that the right domain is correctly distributed"""
        for initial_domain in (self.domains1,self.domains2):
            distributed_domains = self.distributor.distribute(initial_domain)
            self.distributionAssertions(initial_domain,distributed_domains)
            
class NaiveDistributorTC(AbstractDistributorTC):
    def buildDistributor(self):
        return distributors.NaiveDistributor()
    def distributionAssertions(self,initial,distributed):
        assert len(distributed) == 2
        for d in distributed:
            for v in ('v1','v3'):
                assert d[v].getValues() == initial[v].getValues()
        assert distributed[0]['v2'].size() == 1
        assert distributed[1]['v2'].size() == initial['v2'].size()-1

class RandomizingDistributorTC(NaiveDistributorTC):
    def buildDistributor(self):
        return distributors.RandomizingDistributor()
    

class DichotomyDistributorTC(AbstractDistributorTC):
    def buildDistributor(self):
        return distributors.DichotomyDistributor()
    def distributionAssertions(self,initial,distributed):
        assert len(distributed) == 2
        for d in distributed:
            for v in ('v1','v3'):
                assert d[v].getValues() == initial[v].getValues()
        assert distributed[0]['v2'].size() + distributed[1]['v2'].size() == initial['v2'].size() 

class SplitDistributorTC(AbstractDistributorTC):
    def buildDistributor(self):
        return distributors.SplitDistributor(4)
    def distributionAssertions(self,initial,distributed):
        assert len(distributed) == min(4,initial['v2'].size())
        for d in distributed:
            for v in ('v1','v3'):
                assert d[v].getValues() == initial[v].getValues()
        sizes = [d['v2'].size() for d in distributed]
        import operator
        tot_size = reduce(operator.add,sizes)
        assert tot_size == initial['v2'].size() 

class EnumeratorDistributorTC(AbstractDistributorTC):
    def buildDistributor(self):
        return distributors.EnumeratorDistributor()
    def distributionAssertions(self,initial,distributed):
        assert len(distributed) == initial['v2'].size()
        for d in distributed:
            for v in ('v1','v3'):
                assert d[v].getValues() == initial[v].getValues()
            assert d['v2'].size() == 1


def get_all_cases(module):
    import types
    all_cases = []
    for name in dir(module):
        obj = getattr(module, name)
        if type(obj) in (types.ClassType, types.TypeType) and \
               issubclass(obj, TestCase) and \
               not name.startswith('Abstract'):
            all_cases.append(obj)
    all_cases.sort()
    return all_cases

def suite(cases = None):
    import test_distributors
    cases = cases or get_all_cases(test_distributors)
    loader = unittest.defaultTestLoader
    loader.testMethodPrefix = 'test'
    loader.sortTestMethodsUsing = None # disable sorting
    suites = [loader.loadTestsFromTestCase(tc) for tc in cases]
    
    return TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest="suite")
