#!/bin/python
import unittest
import numpy as np
import math

class maxHeap:
    def __init__(self, size):
        self.size=size
        self.content=np.array([None]*size)

    def get_parent(self, ind):
        """
        To get the index of parent of node with index "ind"
        O(1)
        """
        p_ind=math.floor((ind-1)/2)
        if p_ind < 0:
            return None
        return p_ind

    def get_left_child(self, ind):
        """
        To get the index of left child of node with index "ind"
        O(1)
        """
        l_ind=ind*2+1
        if l_ind<self.size:
            return l_ind
        return None

    def get_right_child(self, ind):
        """
        To get the index of right child of node with index "ind"
        O(1)
        """
        r_ind=ind*2+2
        if r_ind<self.size:
            return r_ind
        return None

    def max_heapify(self, key):
        l=self.content[self.get_left_child(key)]
        r=self.content[self.get_right_child(key)]
        largest=key
        if l < self.size and self.content[l]>self.content[largest]:
            largest=l
        if r < self.size and self.content[r]>self.content[largest]:
            largest=r
        if largest!=key:
            self.content[largest], self.content[key]=self.content[key],self.content[largest]

    
    def build_max_heap():
        pass

    def query():
        pass

    def insert():
        pass

    def delete():
        pass

class TestStackQueueMethods(unittest.TestCase):
        def test_init_max_heap(self):
            """
            To test if the heap is initialised correctly
            """
            H=maxHeap(10)
            self.assertEqual(H.size, 10)
            self.assertEqual(len(H.content),10)
            self.assertIsNone(H.content[0])

        def test_get_parent(self):
            """
            To test if the index of the parent node is returned correctly
            """
            H=maxHeap(10)
            self.assertEqual(H.get_parent(0), -1)
            self.assertEqual(H.)
if __name__ == '__main__':
    unittest.main()