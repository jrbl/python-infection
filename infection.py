#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil
import random

def pick_small_N(proportion, pop_size):
    """Select a small random number roughly proportionate to pop_size with ratio proportion.
    
    proportion is a floating point value between 0 and 1
    pop_size is an integer >= 1
    """
    return random.randint(1, int(proportion * pop_size))

def select_N_of(population, count):
    """Return a set of size count members selected from population"""
    return set(random.sample(population, count))

def random_small_sample(population, odds):
    """Select a small number of individuals from population with probability of odds"""
    return set(select_N_of(population, pick_small_N(odds, len(population))))


class User(object):
    AllUserCount = 0

    def __init__(self, *args, **kwargs):
        # XXX: this is convenient when we're still figuring out our API
        #      TODO: get rid of this
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.__id = self.AllUserCount # XXX: Not thread Safe
        self.AllUserCount += 1        # XXX: Yep, still not thread safe
        self.features = set()
        self.coaching = set()
        self.coached_by = set()

    def __hash__(self):
        return self.__id

def limited_infection():
    pass

def total_infection():
    pass

class Population(object):
    def __init__(self, size, infect_rate=0.02, feature=None, coach_rate=0.1, 
                       coach_study_rate=0.5):
        """Initialize a population of Users conforming to certaing statistical properties

        size is a population size
        infect_rate is the rate at which users come pre-infected with some feature
        feature is an optional string representing the infection we want to model
        coach_rate is the rough proportion of Users who coach others
        coach_study_rate is the rough proportion of coaches who also have coaches of their own

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
        self.establish_relationships()

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
        
    def establish_relationships(self):
        students = self.students
        coaches = self.coaches
        for me in students:
            my_coach_pool = coaches if me not in coaches else (coaches - {me})
            my_coach_count = self._random_number_of_coaches(len(my_coach_pool))
            my_coaches = select_N_of(my_coach_pool, my_coach_count)
            for coach in my_coaches:
                coach.coaching.add(me)
                me.coached_by.add(coach)


def main():
    p = Population(size=128, feature="FastThingie")
    return p

if __name__ == "__main__":
    main()
