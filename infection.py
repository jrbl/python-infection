#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil
import random

def pick_small_N(proportion, pop_size):
    """Select a small random number roughly proportionate to pop_size with ratio proportion.
    
    proportion is a floating point value between 0 and 1
    pop_size is an integer >= 1
    """
    range_end = int(proportion * pop_size)
    if range_end == 0:
        return 0
    if range_end < 2:
        return 1
    return random.randint(1, range_end)

def select_N_of(population, count):
    """Return a set of size count members selected from population"""
    count = min(count, len(population))
    if count == 0:
        return set()
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
        User.AllUserCount += 1        # XXX: Not Thread Safe
        self.__id = User.AllUserCount # XXX: Still not thread safe
        self.features = set()
        self.coaching = set()
        self.coached_by = set()

    def __hash__(self):
        return self.__id

    def __repr__(self):
        return "<User() {}>".format(self.__id)


def limited_infection(start_user, max_infections=0):
    """Keep walking across social graph until the entire connected component is infected.
    
    * start_user is the user from whom to start graph traversal; they will be infected along
      with everyone reachable from them. If start_user is none, only traverse from the 
      pre-infected list in population. 
    * max_infections is the target number of users we'd like to be infected. if max_infections 
      is 0, return total_infection(start_user) instead.
    """
    to_infect = {start_user}
    infected_set = set()
    if max_infections == 0:
        return total_infection(start_user=start_user)
    while len(infected_set) < max_infections:
        user = to_infect.pop()
        infected_set.add(user)
        def keyfunc(coach):
            # If we have many coaches, pick the one with the most infected students
            return len( infected_set - coach.coaching )
        if len(user.coached_by) > 1:
            coaches = sorted(user.coached_by, key=keyfunc)
            add_infections = set((coaches.pop(0))).union(user.coaching) - to_infect - infected_set
        else:
            add_infections = user.coached_by.union(user.coaching) - to_infect - infected_set
        to_infect.update(add_infections)
    return infected_set

def total_infection(start_user=None, population=None):
    """Keep walking across social graph until the entire connected component is infected.
    
    * start_user is the user from whom to start graph traversal; they will be infected along
      with everyone reachable from them. If start_user is none, only traverse from the 
      pre-infected list in population. 
    * population is an optional Population object collecting a set of users. Use this to 
      traverse from both the start_user and also from the pre-seeded population infections.
    """
    to_infect = set()
    infected_set = set()
    if start_user is None and population is None:
        raise ValueError, "Both start_user and population may not be unspecified."
    if start_user and not population:
        to_infect.update({start_user})
    if population and not start_user:
        to_infect.update(population.infected)
    while len(to_infect) > 0:
        user = to_infect.pop()
        print "popped {}".format(user)
        infected_set.add(user)
        add_infections = user.coached_by.union(user.coaching) - to_infect - infected_set
        print "enlisting {}".format(add_infections)
        to_infect.update(add_infections)
    return infected_set


class Population(object):
    def __init__(self, users=[]):
        # XXX: this is intended for manual testing and is very slow
        self.N = len(users)
        self.population = users
        self.infected = set([u for u in users if u.features])
        self.coaches = set([u for u in users if u.coaching])
        self.studying_coaches = set([u for u in users if u.coaching and u.coached_by])
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
                coach.coaching.add(me)
                me.coached_by.add(coach)


def main():
    p = Population()
    p.randomize()
    return p

if __name__ == "__main__":
    main()
