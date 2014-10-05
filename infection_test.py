#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Cases for limited_infection() and total_infection()

See SPEC.txt for details.
"""

import unittest

from infection import limited_infection, total_infection, User


class LimitedInfectionTestCase(unittest.TestCase):
    """Test the various calling conventions of limited_infection()

    None of these tests check when max_infections=0 because those checks
    are in TotalInfectionTestCase, below.
    """
    def test_no_user(self):
        """It is an error to call limited_infection without a user object."""
        with self.assertRaises(TypeError):
            limited_infection()

    def test_single_user(self):
        """Limited infection of a single user infects that user as expected."""
        A = User()
        infected = limited_infection(A, 1)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(A, 1e7)
        self.assertEqual(set([A]), infected)

    def test_two_users_with_relation(self):
        """Limited infection of two users behaves well with different limit requests"""
        A = User()
        B = User()
        A.coaching.add(B); B.coached_by.add(A)
        infected = limited_infection(A, 1)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(A, 2)
        self.assertEqual(set([A, B]), infected)
        infected = limited_infection(A, 1e7)
        self.assertEqual(set([A, B]), infected)
        
    def test_two_users_no_relation(self):
        """Limited infection of two independent users treats them independently"""
        A = User()
        B = User()
        infected = limited_infection(A, 1)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(A, 2)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(B, 1e7)
        self.assertEqual(set([B]), infected)

    def test_two_users_cyclic(self):
        """Cyclic users still behave as expected."""
        A = User(); B = User()
        A.coaching.add(B); B.coached_by.add(A)
        A.coached_by.add(B); B.coaching.add(A)
        infected = limited_infection(A, 1)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(A, 2)
        self.assertEqual(set([A, B]), infected)
        infected = limited_infection(A, 1e7)
        self.assertEqual(set([A, B]), infected)
        
    def test_three_users(self):
        """Limited infection of three users behaves well with different limit requests"""
        A = User(); B = User(); C = User()
        A.coaching.add(B); B.coached_by.add(A)
        B.coaching.add(C); C.coached_by.add(B)
        infected = limited_infection(A, 1)
        self.assertEqual(set([A]), infected)
        infected = limited_infection(A, 2)
        self.assertEqual(set([A, B]), infected)
        infected = limited_infection(B, 2)
        self.assertEqual(set([C, B]), infected)
        infected = limited_infection(C, 2)
        self.assertEqual(set([C, B]), infected)
        infected = limited_infection(A, 1e7)
        self.assertEqual(set([A, B, C]), infected)


class TotalInfectionTestCase(unittest.TestCase):
    # TODO: test total infection when calling limited infection here

    def test_no_user(self):
        """It is an error to call limited_infection without a user object."""
        with self.assertRaises(TypeError):
            total_infection()

    def test_single_user(self):
        """Total infection of a single user infects that user as expected."""
        A = User()
        infected = limited_infection(A)
        self.assertEqual(set([A]), infected)

    def test_two_users_with_relation(self):
        """Total infection of two users infects them both regardless of relationship"""
        A = User(); B = User()
        A.coaching.add(B); B.coached_by.add(A)
        infected = total_infection(A)
        self.assertEqual(set([A, B]), infected)
        A.coached_by.add(B); B.coaching.add(A)
        infected = total_infection(A)
        self.assertEqual(set([A, B]), infected)
        A.coaching.clear(); B.coached_by.clear()
        infected = total_infection(A)
        self.assertEqual(set([A, B]), infected)
        
    def test_two_users_no_relation(self):
        """Total infection of two independent users treats them independently"""
        A = User(); B = User()
        infected = total_infection(A)
        self.assertEqual(set([A]), infected)
        infected = total_infection(B)
        self.assertEqual(set([B]), infected)

    def test_three_users(self):
        """Total infection of three users behaves well with different limit requests"""
        A = User(); B = User(); C = User()
        A.coaching.add(B); B.coached_by.add(A)
        infected = total_infection(A)
        self.assertEqual(set([A, B]), infected)
        infected = total_infection(C)
        self.assertEqual(set([C]), infected)
        B.coaching.add(C); C.coached_by.add(B)
        infected = total_infection(A)
        self.assertEqual(set([A, B, C]), infected)
        infected = total_infection(C)
        self.assertEqual(set([A, B, C]), infected)

    def test_limited_single_user_count0(self):
        """Limited infection of count 0 with single user infects that user as expected."""
        A = User()
        infected = limited_infection(A, 0)
        self.assertEqual(set([A]), infected)

    def test_limited_two_users_count0(self):
        """Limited infection of count 0 with two users infects them both"""
        A = User()
        B = User()
        A.coaching.add(B); B.coaching.add(A)
        infected = limited_infection(A, 0)
        self.assertEqual(set([A, B]), infected)
        
    def test_limited_three_users_count0(self):
        """Limited infection of count 0 with three users infects everyone"""
        A = User(); B = User(); C = User()
        A.coaching.add(B); B.coached_by.add(A)
        B.coaching.add(C); C.coached_by.add(B)
        infected = limited_infection(B, 0)
        self.assertEqual(set([A, B, C]), infected)


if __name__ == "__main__":
    unittest.main()
