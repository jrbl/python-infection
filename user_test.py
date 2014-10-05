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
"""Test Cases for User objects"""

import unittest

from user import User


class UserTestCase(unittest.TestCase):
    def test_user_id_unique(self):
        """Every user gets a unique id which is also its hashing key."""
        # XXX: It's understood that these ids aren't threadsafe.
        users = [hash(User()) for i in range(100)]
        self.assertEqual(len(users), len(set(users)))

    def test_add_coach_simple(self):
        """Using student.add_coach(coach) updates student *and* coach"""
        A = User()
        B = User()
        B.add_coach(A)
        self.assertEqual(B.coaches(), set([A]))
        self.assertEqual(A.students(), set([B]))

    def test_add_coach_iterative(self):
        """Using student.add_coach() with a list of coaches updates everybody."""
        A = User()
        coaches = [User() for user in range(5)]
        A.add_coach(coaches)
        self.assertEqual(A._User__coached_by, set(coaches))
        for c in coaches:
            self.assertEqual(c.students(), set([A]))

    def test_add_coach_breaks_without_user(self):
        A = User()
        B = "coach"
        with self.assertRaises(TypeError):
            A.add_coach(B)

    def test_coaches_accessor(self):
        A = User()
        coaches = [User() for user in range(5)]
        A.add_coach(coaches)
        self.assertEqual(A.coaches(), set(coaches))


if __name__ == "__main__":
    unittest.main()
