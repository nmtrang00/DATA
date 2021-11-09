#!/bin/python
from logging import raiseExceptions
import unittest
import numpy as np
import math

"""
Heap:
[i] index of the node in the array
[0]---[2]---[6]...
     |      |
     |      |_[5]...
     |
     |_[1]---[4]...
            |
            |_[3]...
"""
class maxHeap:
    def __init__(self, size=0):
        self.tail=0
        self.size=size
        self.content=np.array([None]*size)

    def get_parent(self, ind):
        """
        To get the index of parent of node with index "ind"
        O(1)
        """
        if ind < 0 or ind >= self.size:
            raise Exception("Error: The index must be in closed range of 0 and size-1")
        p_ind=math.floor((ind-1)/2)
        if p_ind < 0:
            return None
        return p_ind

    def get_left_child(self, ind):
        """
        To get the index of left child of node with index "ind"
        O(1)
        """
        if ind < 0 or ind >= self.size:
            raise Exception("Error: The index must be in closed range of 0 and size-1")
        l_ind=ind*2+1
        if l_ind<self.size:
            return l_ind
        return None

    def get_right_child(self, ind):
        """
        To get the index of right child of node with index "ind"
        O(1)
        """
        if ind < 0 or ind >= self.size:
            raise Exception("Error: The index must be in closed range of 0 and size-1")
        r_ind=ind*2+2
        if r_ind<self.size:
            return r_ind
        return None

    def max_heapify(self, ind):
        """
        To maintain the max-heap property
        O(h)=O(log(n))
        """
        if ind < 0 or ind >= self.tail:
            raise Exception("Error: The index must be in closed range of 0 and tail-1")
        if  self.content[ind]==None:
            raise Exception("Error: The key at this index is None")
        l=self.get_left_child(ind)
        r=self.get_right_child(ind)
        largest=ind
        if l!=None and self.content[l]!=None and self.content[l]>self.content[largest]:
            largest=l
        if r!=None and self.content[r]!=None and self.content[r]>self.content[largest]:
            largest=r
        if largest!=ind:
            self.content[largest], self.content[ind]=self.content[ind],self.content[largest]
            self.max_heapify(largest)
    
    def build_max_heap(self, A):
        """
        To build a max-heap from an array of integer
        The A[0:math.floor((self.size-1)/2)+1] contains roots of all subtree in heap
        => A[math.floor((self.size-1)/2)+1:] contains all leaves of the tree, which is already a root of a maxheap with 1 node.
        Because max_heapify going from top to bottom, we have to traverse in other way arround, 
        else visited nodes at the top are not updated accordingly and the property of maxheap is broken
        
        This function can only be called when the heap is empty:
        +Case 1: The heap currently has size of 0
        +Case 2: The heap with size greater than 0 and empty
        O(nlog(n))
        O(n): tighter bound with the fact that heap has at most ceil(2**(h))
        """
        if self.tail!=0:
            raise Exception("build_max_heap() can only be called when the heap is empty")
        if self.size==0: #Case 1
            self.size=len(A)
            self.content=A
            self.tail=len(A)
        else:
            self.content[:len(A)]=A[:] #Case 2
            self.tail=len(A)
        for i in range(math.floor((self.size-1)/2), -1, -1): 
            self.max_heapify(i)

    def query(self, key):
        """
        To find a number in max-heap
        O(n)
        """
        if key > self.content[0]:
            return None
        for i in range(self.size):
            if self.content[i]==key:
                return i
        return None

    def insert(self, newKey):
        """
        To insert a new key into the heap and then reorder the position of keys if needed 
        to maintain the max-heap property
        O(h)=O(log(n)): for each iteration we traverse through one node on each level of the heap
        """
        if self.tail == self.size:
            raise Exception("OVERFLOW")
        self.content[self.tail]=newKey
        self.tail+=1
        ind=self.tail-1
        p=self.get_parent(ind)
        while p!=None and self.content[p]<self.content[ind]:
            self.content[p], self.content[ind] = self.content[ind], self.content[p]
            ind=p
            p=self.get_parent(ind)

    def extract_max(self):
        pass

    def delete(self):
        pass

class TestStackQueueMethods(unittest.TestCase):
    def test_init_max_heap(self):
        """
        To test if the heap is initialised correctly
        """
        H=maxHeap(size=7)
        self.assertEqual(H.size, 7)
        self.assertEqual(len(H.content),7)
        self.assertIsNone(H.content[0])
        self.assertEqual(H.tail,0)

    def test_get_parent(self):
        """
        To test if the index of the parent is returned correctly
        """
        H=maxHeap(size=7)
        with self.assertRaises(Exception): H.get_parent(-1)
        with self.assertRaises(Exception): H.get_parent(7)
        self.assertEqual(H.get_parent(0), None)
        self.assertEqual(H.get_parent(6), 2)

    def test_get_left_child(self):
        """
        To test if the index of the left child is returned correctly
        """
        H=maxHeap(size=7)
        with self.assertRaises(Exception): H.get_left_child(-1)
        with self.assertRaises(Exception): H.get_left_child(7)
        self.assertEqual(H.get_left_child(6), None)
        self.assertEqual(H.get_left_child(2), 5)

    def test_get_right_child(self):
        """
        To test if the index of the right child is returned correctly
        """
        H=maxHeap(size=7)
        with self.assertRaises(Exception): H.get_right_child(-1)
        with self.assertRaises(Exception): H.get_right_child(7)
        self.assertEqual(H.get_right_child(6), None)
        self.assertEqual(H.get_right_child(2), 6)

    def test_max_heapify(self):
        """
        To test if heapify works correctly with a simple heap of 3 elements
        (1)---(3)
                |
                |_(2)
        """
        H=maxHeap(size=4)
        H.content[0]=1
        H.content[1]=2
        H.content[2]=3
        H.tail=3
        with self.assertRaises(Exception): H.max_heapify(-1)
        with self.assertRaises(Exception): H.max_heapify(7)
        with self.assertRaises(Exception): H.max_heapify(3)
        H.max_heapify(2)
        self.assertEqual(H.content[0],1)
        self.assertEqual(H.content[1],2)
        self.assertEqual(H.content[2],3)
        H.max_heapify(0)
        self.assertEqual(H.content[0],3)
        self.assertEqual(H.content[1],2)
        self.assertEqual(H.content[2],1)

    def test_build_max_heap_0(self):
        """
        To test if a max heap is built correctly from an array of int when it currently has a size of 0,
        and error is raised if the heap is not empty
        """
        H=maxHeap()
        H.build_max_heap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
        self.assertEqual(H.content,[16, 14, 10, 8, 7, 9, 3, 2, 4, 1])
        self.assertEqual(H.size, 10)
        self.assertEqual(H.tail, 10)
        with self.assertRaises(Exception): H.build_max_heap([1])
    
    def test_build_max_heap_1(self):
        """
        To test if a max heap is built correctly from an array of int,
        when it size greater than 0 and empty
        """
        H=maxHeap(size=20)
        H.build_max_heap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
        # print(H.content[0:10])
        # print(type(H.content[0:10]))
        expected_arr=[16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
        for i in range(10):
            self.assertEqual(H.content[i],expected_arr[i])
        self.assertEqual(H.size, 20)
        self.assertEqual(H.tail, 10)
    
    def test_init_max_heap_with_array(self):
        """
        To test if a max heap is built correctly when the heap is initialised with an array
        """
        H=maxHeap()
        H.build_max_heap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
        self.assertEqual(H.content,[16, 14, 10, 8, 7, 9, 3, 2, 4, 1])
        self.assertEqual(H.size, 10)

    def test_query(self):
        """
        To test if the correct index is returned when the key is in the heap,  
        None is returned when not or the key greater than max key of the heap
        """
        H=maxHeap() #content=[16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
        H.build_max_heap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
        self.assertEqual(H.query(4),8)
        self.assertEqual(H.query(17), None)

    def test_insert_0(self):
        """
        To test if exception is raised when a new key is inserted and the heap is already full
        """
        H=maxHeap()
        H.build_max_heap([1,2,3])
        with self.assertRaises(Exception): H.insert(4)
    
    def test_insert_1(self):
        """
        To test if a new key is correctly inserted into a simple maxheap
        (0) ===> (1)---NIL  ===> (2)---(1)
                      |               |
                      |_(0)           |_(0)
        """
        H=maxHeap(size=10)
        H.insert(0)
        self.assertEqual(H.content[0], 0)
        self.assertEqual(H.tail, 1)
        H.insert(1)
        self.assertEqual(H.content[0], 1)
        self.assertEqual(H.tail, 2)
        H.insert(2)
        self.assertEqual(H.content[0], 2)
        self.assertEqual(H.content[1], 0)
        self.assertEqual(H.content[2], 1)
        self.assertEqual(H.tail, 3)

    def test_insert_2(self):
        """
        To test if a new key is correctly inserted into a maxheap of size 10 that already contains 7 keys
        (0)
        """
        H=maxHeap(size=10)
        H.build_max_heap([16, 14, 10, 8, 7, 9, 3])
        H.insert(17)
        expected_arr=[17, 16, 10, 14, 7, 9 ,3, 8]
        for i in range(7):
            self.assertEqual(H.content[i], expected_arr[i])

if __name__ == '__main__':
    unittest.main()