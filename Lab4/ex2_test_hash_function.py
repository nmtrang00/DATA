#!/bin/python
from random import randint
from scipy.stats import wilcoxon
"""
To assess the collision rate in the dictionary, we need to define some parameters in the dictionary:

- Number of items to be stored: n=10**3
- Range of keys: 0≤k≤10**4
- Number of available slots in the dictionary: m=3 => slots: 0, 1, 2
"""

def hash_function_devision(x):
    return x%20

def hash_function_universal(x):
    return ((4*x+1)%10007)%20

def calculate_avg_collision_rate(function_to_test):
    slots=[0]*20 #Init an array to store the number of item in each slot
    for i in range(1000):
        x=randint(0, 10**4)
        hashed_x=function_to_test(x)
        slots[hashed_x]+=1
    return slots

def p_value(rel_stats):
    """
    To format result from scipy.stats
    """
    return float(str(rel_stats).split(",")[1].split(")")[0].split("=")[1])

def compare_collision_rate():
    """
    Two-sided t_test
    H0: There is no significance difference in collision distribution when using hash_function_division and hash_function_universal
    """
    for i in range(5):
        D=calculate_avg_collision_rate(hash_function_devision)
        U=calculate_avg_collision_rate(hash_function_universal)
        # print(D, U)
        rel_stats=wilcoxon(D,U,alternative="two-sided",mode="approx")
        p_val=p_value(rel_stats)
        if p_val<=0.05:
            print("Attempt no.{}: p_value={:.2f}; H0 rejected".format(i+1, p_val))
        else:
            print("Attempt no.{}: p_value={:.2f}; H0 NOT rejected".format(i+1, p_val))

compare_collision_rate()