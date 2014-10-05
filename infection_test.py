#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest


# Testing goal: A, B, and C are the only users and they share no coaching
# relationship. total_infection(A) results in only A becoming infected.
# limited_infection(A, 3) results in all three becoming infected.
#
# A coaches B coaches C. total_infection(A), total_infection(B), and
# total_infection(C) each result in everyone becoming infected.
# limited_infection(A, 2) results in A and B becoming infected.

class TestLimitedInfection(unittest.TestCase):
    pass

class TestTotalInfection(unittest.TestCase):
    pass

def limited_infection():
    pass

def total_infection():
    pass

def main():
    pass


if __name__ == "__main__":
    main()
