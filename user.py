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
"""Implement User() class for use by infection.py and friends"""


from collections import Iterable


class User(object):
    AllUserCount = 0

    def __init__(self, *args, **kwargs):
        # XXX: this is convenient when we're still figuring out our API
        #      TODO: get rid of this
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        User.AllUserCount += 1        # XXX: Not Thread Safe
        self.__id = User.AllUserCount # XXX: Still not thread safe
        self.features = set()
        self.__coaching = set()
        self.__coached_by = set()

    def add_coach(self, coach):
        """Symmetrically add coached_by to us and coaching to them.
        
        If coach is an iterable, every member will be added.
        It is an error to add a coach which is not a User."""
        self._add_user(coach, '_User__coached_by', '_User__coaching')

    def add_student(self, student):
        """Symmetrically add coaching to us and coached_by to them.
        
        If student is an iterable, every member will be added.
        It is an error to add a student which is not a User."""
        self._add_user(student, '_User__coaching', '_User__coached_by')

    def _add_user(self, userish, ourtarget, theirtarget):
        def add_with_check(userish):
            if isinstance(userish, User):
                v = getattr(self, ourtarget)
                v.add(userish)
                setattr(self, ourtarget, v)
                v = getattr(userish, theirtarget)
                v.add(self)
                setattr(userish, theirtarget, v)
            else:
                raise TypeError, "Only Users can be coaches."
        if isinstance(userish, Iterable):
            for u in userish:
                add_with_check(u)
        else:
            add_with_check(userish)

    def coaches(self):
        """Return the set of coaches this user is coached_by"""
        return self.__coached_by

    def students(self):
        """Return the set of students this user is coaching"""
        return self.__coaching

    def __hash__(self):
        return self.__id

    def __repr__(self):
        return "<User() {}>".format(self.__id)

