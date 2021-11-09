#!/bin/python
import numpy as np
from numpy.random import randint
from numpy.random.mtrand import random
from scipy.stats import wilcoxon

from ex1_stack import Stack as Stack_array
from ex2_queue import Queue as Queue_array
from ex4_stack_queue_linked_list import Stack as Stack_list
from ex4_stack_queue_linked_list import Queue as Queue_list

import sys
import os
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
"""
I choose Wilcoxin as the core method for the comparative tests.
For each test, I generate n pairs of runtime, 
one from function implemented with array and one from function implemented with list.
NOTES:
Wilcoxin does not rely on assumptions that data comes from a particular parameterized distribution
wilcoxin(x,y) => diff=x-y
The two-sided test's H0: The median of the differences is zero against the alternative that it is different from zero. 
The one-sided test's H0: The median is positive against the alternative that it is negative (alternative == 'less'), or vice versa (alternative == 'greater.').
"""
class compare_stack():
    def __init__(self, no_test):
        self.no_size=no_test

    def compare_emptyStack(self):
        """
        Two-sided Wilcoxin
        H0: Implementing stack with array and implementing stack with singly link list do not express significant difference in running time
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        S_arr=Stack_array(self.no_size)
        S_list=Stack_list()
        for i in range(self.no_size):
            S_arr.push(i)
            S_list.push(i)
            A.append(track_time(S_arr.stackEmpty()))
            L.append(track_time(S_list.stackEmpty()))
        rel_stats=wilcoxon(A,L,alternative="two-sided")
        return p_value(rel_stats)

    def compare_push(self):
        """
        Two-sided Wilcoxin
        H0: Implementing stack with array and implementing stack with singly link list do not express significant difference in running time
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        S_arr=Stack_array(self.no_size+1)
        S_list=Stack_list()
        for i in range(self.no_size):
            A.append(track_time(S_arr.push(i)))
            L.append(track_time(S_list.push(i)))
        rel_stats=wilcoxon(A,L,alternative="two-sided")
        return p_value(rel_stats)
    
    def compare_pop(self):
        """
        Two-sided Wilcoxin
        H0: Implementing stack with array and implementing stack with singly link list do not express significant difference in running time
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        S_arr=Stack_array(self.no_size)
        S_list=Stack_list()
        for i in range(self.no_size):
            S_arr.push(i)
            S_list.push(i)
            A.append(track_time(S_arr.pop()))
            L.append(track_time(S_list.pop()))
        rel_stats=wilcoxon(A,L,alternative="two-sided")
        return p_value(rel_stats)

    def compare_peek(self):
        """
        Two-sided Wilcoxin
        H0: Implementing stack with array and implementing stack with singly link list do not express significant difference in running time
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        S_arr=Stack_array(self.no_size)
        S_list=Stack_list()
        for i in range(self.no_size):
            S_arr.push(i)
            S_list.push(i)
            A.append(track_time(S_arr.pop()))
            L.append(track_time(S_list.pop()))
        rel_stats=wilcoxon(A,L,alternative="two-sided")
        return p_value(rel_stats)


class compare_queue():
    def __init__(self, no_test):
        self.no_size=no_test
        
    def compare_enqueue(self):
        """
        Two-sided Wilcoxin
        H0: Implementing queue with array and implementing queue with singly link list do not express significant difference in running time
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        Q_arr=Queue_array(self.no_size)
        Q_list=Queue_list()
        for i in range(1,self.no_size):
            A.append(track_time(Q_arr.enqueue(i)))
            L.append(track_time(Q_list.enqueue(i)))
        rel_stats=wilcoxon(A,L,alternative="two-sided")
        return p_value(rel_stats)

    def compare_dequeue(self):
        """
        One-sided Wilcoxin
        H0: Implementing queue with array is more efficient than implementing queue with singly link list
        (The median difference in runtime of 2 implementations (T_arr-T_list) is negative)
        For each iternation, a new element is pushed to the stack, which means the stack size increases by one.
        """
        A=[]
        L=[]
        Q_arr=Queue_array(self.no_size)
        Q_list=Queue_list()
        for i in range(1,self.no_size):
            Q_arr.enqueue(i)
            Q_list.enqueue(i)
            A.append(track_time(Q_arr.dequeue()))
            L.append(track_time(Q_list.dequeue()))
        rel_stats=wilcoxon(A,L,alternative="greater")
        return p_value(rel_stats)

def main():
    for i in range(1,11):
        print("Attempt no.{}:".format(i))
        S=compare_stack(5000)
        print("\tp_value_emptyStack:", round(S.compare_emptyStack(),5))
        print("\tp_value_push:", round(S.compare_push(),5))
        print("\tp_value_pop:", round(S.compare_pop(),5))
        print("\tp_value_peek:", round(S.compare_peek(),5))
        Q=compare_queue(5000)
        print("\tp_value_enqueue:", round(Q.compare_enqueue(),5))
        print("\tp_value_dequeue:", round(Q.compare_dequeue(),5))

main()