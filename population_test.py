#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Joseph Blaylock <jrbl@jrbl.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implement Population test cases"""


import unittest

from population import select_N_of, random_small_sample, Population
from user import User


class UtilityTestCase(unittest.TestCase):
    """Test the small utility methods in population.py"""
    def test_select_N_of(self):
        """Test the 0, 1 and many cases for select_n_of()"""
        pop0 = []
        pop1 = [1]
        popmany = range(10)
        self.assertEqual(set(), select_N_of(pop0, 0))
        self.assertEqual(set(), select_N_of(pop0, 1))
        self.assertEqual(set(), select_N_of(pop0, 1e7))
        self.assertEqual(set([]), select_N_of(pop1, 0))
        self.assertEqual(set([1]), select_N_of(pop1, 1))
        self.assertEqual(set([1]), select_N_of(pop1, 1e7))
        self.assertEqual(set([]), select_N_of(popmany, 0))
        popmany_1 = select_N_of(popmany, 1)
        self.assertEqual(len(popmany_1), 1)
        self.assertTrue(popmany_1.pop() in popmany)
        self.assertEqual(len(select_N_of(popmany, 1e7)), 10)

    def test_random_small_sample(self):
        """Test the 0, 1, and many cases for test_random_small_sample()"""
        pop0 = []
        pop1 = [1]
        popmany = range(10)
        self.assertEqual(set(), random_small_sample(pop0, 0.80))
        self.assertEqual(set(pop1), random_small_sample(pop1, 0.80))
        self.assertEqual(set(popmany), random_small_sample(popmany, 1))
        self.assertEqual(set(pop0), random_small_sample(popmany, 0))
        popmany_50 = random_small_sample(popmany, 0.50)
        self.assertLess(len(popmany_50), len(popmany))
        self.assertGreater(len(popmany_50), 0)

    def test_random_small_sample_error(self):
        """test_random_small_sample() raises ValueError with invalid odds"""
        with self.assertRaises(ValueError):
            random_small_sample([], 1e7)


class PopulationTestCase(unittest.TestCase):
    def test_empty_population_creation(self):
        p = Population()
        self.assertEqual(0, p.N)
        self.assertEqual(p.N, len(p.population))
        self.assertEqual(set(), p.infected)
        self.assertEqual(set(), p.coaches)
        self.assertEqual(set(), p.students)

    def test_lonely_population_creation(self):
        unlucky = User()
        unlucky.features.add('very very unlucky')
        p = Population(users=[unlucky])
        self.assertEqual(1, p.N)
        self.assertEqual(p.N, len(p.population))
        self.assertEqual(set([unlucky]), p.infected)
        self.assertEqual(set(), p.coaches)
        self.assertEqual(set([unlucky]), p.students)

    def test_pessimistic_random_population_creation(self):
        p = Population()
        # 10 students who are all infected, all teachers, and all study
        p.randomize(10, infect_rate=1, feature='A', coach_rate=1, coach_study_rate=1)
        self.assertEqual(10, p.N)
        self.assertEqual(p.N, len(p.population))
        self.assertEqual(len(p.population), len(p.infected))
        self.assertEqual(len(p.infected), len(p.students))
        self.assertEqual(len(p.students), len(p.coaches))

    def test_normal_random_population_creation(self):
        # XXX: I suppose it's possible these asserts could fail because we're dealing with
        #      probabalistic outcomes; I haven't taken the time to prove these always work
        p = Population()
        p.randomize(1024)
        self.assertLess(len(p.coaches), len(p.students))
        self.assertLess(len(p.studying_coaches), len(p.coaches))
        self.assertLess(1, max([len(u.coaches()) for u in p.students]))


if __name__ == "__main__":
    unittest.main()
