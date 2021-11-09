#!/bin/python
import numpy as np
import unittest

"""
Python does not support built-in array; therefore, I used numpy.array instead.
push(), pop(), and peek() functions are included
"""

class Stack():
    def __init__(self, size):
        self.top=-1
        self.size=size
        self.content=np.array([np.nan]*size)

    def stackEmpty(self):
        """
        To check if the stack is empty
        O(1)
        """
        if self.top==-1: 
            return True
        else:
            return False

    def push(self, newNumber):
        """
        To add an element to the stack
        O(1)
        """
        if self.top>=self.size:
            raise Exception("Overflow")
        else:
            self.top+=1
            self.content[self.top]=newNumber

    def pop(self):
        """
        To get value and remove the most recently added element in the stack
        O(1)
        """
        if self.stackEmpty(): 
            raise Exception("Underflow") 
        else:
            self.top-=1 
            return self.content[self.top+1]

    def peek(self):
        """
        To get value of the most recently added element in the stack
        O(1)
        """
        if self.stackEmpty():
            raise Exception("Underflow")
        else:
            return self.content[self.top]

class TestStackMethods(unittest.TestCase):

    def test__init_top(self):
        """
        To test if the Stack.top is correctly set to -1 when initialising
        """
        S=Stack(5)
        self.assertEqual(S.top, -1)
    
    def test__init_size(self):
        """
        To test if an array of desired "size" is created when initialising
        """
        S=Stack(5)
        self.assertEqual(S.content.shape[0], 5)

    def test__init_content(self):
        """
        To test if an nan array is created when initialising
        """
        S=Stack(5)
        self.assertEqual(sum(np.isnan(S.content)),5)

    def test_push0(self):
        """
        To test if Stack.top and Stack.content are updated
        when an item is pushed to the stack
        """
        S=Stack(5)
        top_init=S.top
        S.push(10)
        self.assertEqual(S.top,top_init+1)
        self.assertEqual(S.content[0],10)
        top_init_1=S.top
        S.push(20)
        self.assertEqual(S.top,top_init_1+1)
        self.assertEqual(S.content[1],20)

    def test_push1(self):
        """
        To test if "Overflow" is raised
        when an item is pushed to the stack that is fully filled
        The function is wrapped so that its result is returned to 
        assertRaises() to be assessed.
        """
        S=Stack(2)
        S.push(10)
        S.push(20)
        with self.assertRaises(Exception): S.push(30)

    def test_pop_0(self):
        """
        Case 0:
        To test if the exception is throwed when pop() is called 
        and the stack is empty
        The function is wrapped so that its result is returned to 
        assertRaises() to be assessed.
        """
        S=Stack(5)
        with self.assertRaises(Exception): S.pop()
    
    def test_pop_1(self):
        """
        Case 1:
        To test if S.top is updated and the item formerly at the 
        top is returned, when pop() is called and the stack is not empty
        """
        S=Stack(5)
        S.push(10)
        top_old=S.top
        self.assertEqual(S.pop(),10)
        self.assertEqual(S.top,top_old-1)

    def test_peek_0(self):
        """
        Case 0:
        To test if the exception is throwed when peek() is called 
        and the stack is empty
        The funtion is wrapped so that its result is returned to 
        assertRaises() to be assessed.
        """
        S=Stack(5)
        with self.assertRaises(Exception): S.peek()

    def test_peek_1(self):
        """
        Case 1:
        To test if the item at the top (entering last) is returned, 
        but Stack.top is unchanged when pop() is called and the stack is not empty
        """
        S=Stack(5)
        S.push(10)
        S.push(20)
        top_old=S.top
        self.assertEqual(S.peek(),20)
        self.assertEqual(S.top,top_old)

    def test_stackEmpty_0(self):
        """
        Case 0:
        To test if "True" is returned when the stack is empty at initialisation 
        or after all items are popped out
        """
        S=Stack(5)
        self.assertTrue(S.stackEmpty())
        S.push(1)
        S.push(2)
        S.pop()
        S.pop()
        self.assertTrue(S.stackEmpty())

    def test_stackEmpty_1(self):
        """
        Case 1:
        To test if "False" is returned when items are pushed to the Stack
        """
        S=Stack(5)
        S.push(1)
        self.assertFalse(S.stackEmpty())
        S.push(2)
        self.assertFalse(S.stackEmpty())

if __name__ == '__main__':
    unittest.main()

