#!/bin/python
import numpy as np
import unittest

"""
Python does not support built-in array; therefore, I used numpy.array instead.
enqueue() and dequeue() functions are included
"""

class Queue():
    def __init__(self, size):
        self.head=0
        self.tail=0
        self.size=size
        self.content=np.array([np.nan]*size)

    """
    Overflow and underflow happen when Q.head==Q.tail
    We can detect underflow when dequeue() is called right after initialisation and nan is returned
    Later, it is hard to distinguish overflow and underflow,
    because we do not actually delete or change the data stored in the memory that is previously dequeued.
    """
    
    def enqueue(self, newNumber):
        """
        To add a new element to the tail of the queue
        O(1)
        """
        self.content[self.tail]=newNumber
        if self.tail == self.size-1: #self.content.shape[0]=self.size
            self.tail=0
        else:
            self.tail+=1
    
    def dequeue(self):
        """
        To remove the earliest added element out of the queue
        O(1)
        """
        result=self.content[self.head]
        if self.head == self.size-1: #self.content.shape[0]=self.size
            self.head=0
        else:
            self.head+=1
        return result
    
class TestQueueMethods(unittest.TestCase):

    def test__init_head_tail(self):
        """
        To test if the Queue.head and Queue.tail are correctly set to 0 when initialising
        """
        Q=Queue(5)
        self.assertEqual(Q.head, 0)
        self.assertEqual(Q.tail,0)
    
    def test__init_size(self):
        """
        To test if an array of desired "size" is created when initialising
        """
        Q=Queue(5)
        self.assertEqual(Q.content.shape[0], 5)

    def test__init_content(self):
        """
        To test if an nan array is created when initialising
        """
        Q=Queue(5)
        self.assertEqual(sum(np.isnan(Q.content)),5)

    def test_enqueue_0(self):
        """
        Case 0:
        To test if Q.content and Q.tail are updated after a number is enqueued
        and Q.tail does not point to the last place in the array
        """
        Q=Queue(5)
        old_tail=Q.tail
        Q.enqueue(10)
        self.assertEqual(Q.content[0],10)
        self.assertEqual(Q.tail,old_tail+1)
        Q.enqueue(20)
        self.assertEqual(Q.tail, 2)
        self.assertEqual(Q.head,0)

    def test_enqueue_1(self):
        """
        Case 1:
        To test if Q.content is updated and Q.tail is 0 after a number is enqueued
        and Q.tail points to the last place in the array
        """
        Q=Queue(5)
        for i in range(4):
            Q.enqueue(i)
        self.assertTrue(np.array_equal(Q.content,np.array([0,1,2,3,np.nan]),equal_nan=True))
        self.assertEqual(Q.tail, 4)
        Q.enqueue(100)
        self.assertEqual(Q.tail,0)

    def test_dequeue_0(self):
        """
        Case 0:
        To test if nan is returned when dequeue() is called right after initialisation and underflow happens 
        """
        Q=Queue(5)
        old_head=Q.head
        self.assertTrue(np.isnan(Q.dequeue())) #Underflow
        self.assertEqual(Q.head,1) 
        self.assertEqual(Q.head, old_head+1)
    
    def test_dequeue_1(self):
        """
        Case 1:
        To test if the item entering first is returned, Q.head is updated, when a number is dequeued
        and Q.head does not point to the last place in the array
        """
        Q=Queue(5)
        Q.enqueue(10)
        Q.enqueue(20) 
        old_head=Q.head
        self.assertEqual(Q.dequeue(),10)
        self.assertEqual(Q.head,old_head+1)
        self.assertEqual(Q.head,1)
    
    def test_dequeue_2(self):
        """
        Case 2:
        To test if the item entering first is returned, Q.head is 0 , when a number is dequeued
        and Q.head points to the last place in the array
        """
        Q=Queue(5)
        for i in range(5):
            Q.enqueue(i)
        self.assertTrue(np.array_equal(Q.content,np.array([0,1,2,3,4]),equal_nan=True))
        self.assertEqual(Q.head, 0)
        #Dequeue the first 4 numbers, so that Q.head points to the last place in the array
        for i in range(4):
            self.assertEqual(Q.dequeue(),i)
        self.assertEqual(Q.head,4)
        Q.dequeue()
        self.assertEqual(Q.head,0)

if __name__ == '__main__':
    unittest.main()
