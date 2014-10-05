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
"""Implement total_infection() and local_infection() for User objects

Relies on some graph of User objects to be pre-generated; check out User
and Population, and read the unit tests for some ideas.
"""


def limited_infection(start_user, max_infections=0):
    """Keep walking across social graph until the entire connected component is infected.
    
    * start_user is the user from whom to start graph traversal; they will be infected along
      with everyone reachable from them. If start_user is none, only traverse from the 
      pre-infected list in population. 
    * max_infections is the target number of users we'd like to be infected. if max_infections 
      is 0, return total_infection(start_user) instead.
    """
    to_infect = set([start_user])
    infected_set = set()
    if max_infections == 0:
        return total_infection(start_user=start_user)
    while len(infected_set) < max_infections:
        try:
            user = to_infect.pop()
        except KeyError:
            # pop from empty set means our population is smaller than max_infections
            # so just return whatever we've calculated so far
            return infected_set
        infected_set.add(user)
        def keyfunc(coach):
            # If we have many coaches, pick the one with the most infected students
            return len( infected_set - coach.students() )
        if len(user.coaches()) > 1:
            coaches = sorted(user.coaches(), key=keyfunc)
            add_infections = set((coaches.pop(0))).union(user.students()) - to_infect - infected_set
        else:
            add_infections = user.coaches().union(user.students()) - to_infect - infected_set
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
        raise TypeError, "Both start_user and population may not be unspecified."
    if start_user and not population:
        to_infect.update({start_user})
    if population and not start_user:
        to_infect.update(population.infected)
    while len(to_infect) > 0:
        user = to_infect.pop()
        infected_set.add(user)
        add_infections = user.coaches().union(user.students()) - to_infect - infected_set
        to_infect.update(add_infections)
    return infected_set

