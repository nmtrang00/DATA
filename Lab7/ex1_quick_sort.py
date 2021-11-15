#!/bin/python

import unittest
from numpy.random import randint

def partition(A, start, end):
    """
    Top rearrange the subarray A[start: end] in place,
    so that all numbers smaller or equal to A[end-1], the pivot
    are on its left, while greater numbers are on its right.
    Loop invariant:
    1. A[k] <= pivot, start<=k<anchor
    2. A[k] > pivot, anchor<=k<end-1
    3. A[end-1]=pivot
    """
    if start==end-1: #Only an element in the array
        return A, start
    pivot=A[end-1]
    anchor=start #A[anchor:start]=[]
    for j in range(start, end-1):
        if A[j]<=pivot:
            A[j], A[anchor] = A[anchor], A[j]
            anchor+=1
    A[anchor], A[end-1] = A[end-1], A[anchor]
    return A, anchor

def quickSort(A, start, end):
    """
    To sort a subarray A[start: end]
    """
    if start<end-1:
        A, anchor=partition(A, start, end)
        quickSort(A, start, anchor)
        quickSort(A, anchor+1, end)
    return A

class TestStackQueueMethods(unittest.TestCase):
    def test_partition(self):
        A=[0,2,8,7,1,3,5,6,4]
        expected_arr=[0,2,1,3,4,7,5,6,8]
        rel, anchor=partition(A,0,len(A))
        self.assertEqual(rel, expected_arr)
        self.assertEqual(anchor, 4)

    def test_quickSort_0(self):
        A=[0,2,8,7,1,3,5,6,4]
        self.assertEqual(sorted(A),quickSort(A,0,len(A)))

    def test_quickSort_1(self):
        A=[0,2,8,7,1,4,8,3,5,6,4]
        self.assertEqual(sorted(A),quickSort(A,0,len(A)))

    def test_quickSort_2(self):
        for i in range(100):
            A=list(randint(0, i*2, i))
            self.assertEqual(sorted(A),quickSort(A,0,len(A)))
if __name__ == '__main__':
    unittest.main()