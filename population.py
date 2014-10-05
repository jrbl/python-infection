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
"""Implement Population class for fun testing"""


from math import ceil
import random

from user import User


def select_N_of(population, count):
    """Return a set of size count members selected from population"""
    count = min(count, len(population))
    if count == 0:
        return set()
    return set(random.sample(population, count))

def random_small_sample(population, odds):
    """Select a small random number of individuals from population with probability of odds

    population is the collection of objects to select among
    odds is a floating point value between 0 and 1

    The idea here is that we use odds to determine the discrete number of
    samples we want, and then we get exactly that number of samples. We could
    apply a uniform distribution across the population and take everything
    above or below a threshold, but this works almost as well is more readable.
    """
    N = 1
    if odds < 0 or odds > 1:
        raise ValueError, "Odds must be a value between 0 and 1"
    elif odds == 0:
        return set()
    elif odds == 1:
        return set(population)
    range_end = int(odds * len(population))
    if range_end >= 2:
        N = random.randint(1, range_end)
    return set(select_N_of(population, N))


class Population(object):
    def __init__(self, users=[]):
        # XXX: this is intended for manual testing and is very slow; it's best to 
        #      initialize an empty users list and use randomize() to get big datasets
        self.N = len(users)
        self.population = users
        self.infected = set([u for u in users if u.features])
        self.coaches = set([u for u in users if u.students()])
        self.studying_coaches = set([u for u in users if u.students() and u.coaches()])
        self.students = set(users) - (self.coaches - self.studying_coaches)

    def randomize(self, size, infect_rate=0.02, feature=None, coach_rate=0.1, 
                        coach_study_rate=0.5, classes_per_student=0):
        """Initialize a population of Users conforming to certaing statistical properties

        * size is a population size
        * infect_rate is the rate at which users come pre-infected with some feature
        * feature is an optional string representing the infection we want to model
        * coach_rate is the rough proportion of Users who coach others
        * coach_study_rate is the rough proportion of coaches who also have coaches of 
          their own
        * classes_per_student set a precise number of coaches for each student

        XXX: currently Population only supports modeling one feature at a time, despite 
             Users being able to carry an arbitrary set of features.
        """
        self.N = size
        pop = [User() for x in xrange(size)]
        self.population = pop
        self.infected = random_small_sample(pop, infect_rate)
        coaches = random_small_sample(pop, coach_rate)
        self.coaches = coaches
        studying_coaches = random_small_sample(coaches, coach_study_rate)
        self.studying_coaches = studying_coaches
        # students are everybody except the coaches who don't study
        self.students = set(pop) - (coaches - studying_coaches)

        if feature is not None:
            self.toggle_infections(feature)
        self.update_user_relationships(classes_per_student)

    def _random_number_of_coaches(self, max_poolsize):
        # I'm guessing most students take 1 course, and a handful take more
        # but almost none take more than 6 or so.
        return int(ceil(abs(random.normalvariate(mu=1, sigma=0.9))))

    def toggle_infections(self, feature=None):
        """If feature specified, enable it for every poplutaion member in infected set.

        If feature is None, remove all infections everywhere."""
        if feature is not None:
            for user in self.infected:
                user.features.add(feature)
        else:
            for user in self.population:
                user.features.clear()
        
    def update_user_relationships(self, classes_per_student=0):
        students = self.students
        coaches = self.coaches
        for me in students:
            my_coach_pool = coaches if me not in coaches else (coaches - {me})
            my_coach_count = classes_per_student if classes_per_student else self._random_number_of_coaches(len(my_coach_pool))
            my_coaches = select_N_of(my_coach_pool, my_coach_count)
            for coach in my_coaches:
                me.add_coach(coach)
