#!/bin/python
import numpy as np
import unittest
from ex3_singly_linked_list import singly_linked_list, node

"""
Python does not support built-in array; therefore, I used numpy.array instead.
push(), pop(), and peek() functions are included
"""

class Stack():
    def __init__(self):
        self.content=singly_linked_list()

    def stackEmpty(self):
        """
        To check if the stack is empty, ie. Stack.content.head is not linked to another node
        but np.nan as the characteristic inherited from the singly linked list
        O(1)
        """
        if not isinstance(self.content.head, node):
            return True
        else:
            return False

    def push(self, newNumber):
        """
        To add an element to the stack
        O(1): list.insert() runs in O(1)
        """
        self.content.insert(newNumber)

    def pop(self):
        """
        To remove the most recently added node, ie. node_0
        O(1): list.delete() runs in O(n)
        However, when we delete the first node, ie. case List.head.key == key_to_remove,
        list.delete_by_node() runs in constant time, Ω(1).
        """
        if self.stackEmpty():
            raise Exception("Underflow")
        else:
            node_to_pop_key=self.content.head.key
            self.content.delete(node_to_pop_key)
            return node_to_pop_key

    def peek(self):
        """
        To get value of the most recently added node in the stack
        O(1)
        """
        if self.stackEmpty():
            raise Exception("Underflow")
        else:
            return self.content.head.key

class Queue():
    def __init__(self):
        self.content=singly_linked_list()
    
    """
    Overflow does not happen because we can extend the list if needed for space for new element
    Underflow when there is no element to dequeue(), ie. list.head =np.nan, not a node
    """

    def enqueue(self, newNumber):
        """
        To add a new element to the tail of the queue, ie. to the front of the list
        O(1): list.insert() runs in O(1)
        """
        self.content.insert(newNumber)
    
    def dequeue(self):
        """
        To remove the earliest added element out of the queue, ie. the last element in the list
        O(n)
        """
        if not isinstance(self.content.head, node):
            raise Exception("There is no element in the queue.")
        else:
            if not isinstance(self.content.head.next, node):
                node_to_remove=self.content.head
                self.content.head=node_to_remove.next #=np.nan
                node_to_remove.next=np.nan
                return node_to_remove.key
            else:
                node_prev=self.content.head
                node_to_remove=self.content.head.next
                while isinstance(node_to_remove.next, node): 
                    #Different condition from List.delete() 
                    # because in List.delete() the loop stops when the matching key is found 
                    node_prev=node_to_remove
                    node_to_remove=node_to_remove.next
                node_prev.next=node_to_remove.next #=np.nan 
                return node_to_remove.key

class TestStackQueueMethods(unittest.TestCase):

    def test_stack_init(self):
        """
        To test if the Stack.content is correctly initialised as a singly linked list
        """
        S=Stack()
        self.assertTrue(isinstance(S.content, singly_linked_list))
    
    def test_push(self):
        """
        To test if Stack.content is updated when an item is pushed to the stack
        """
        S=Stack()
        S.push(10)
        #S=10
        self.assertEqual(S.content.head.key, 10)
        S.push(20)
        #S=20, 10
        self.assertEqual(S.content.head.key, 20)

    def test_pop_0(self):
        """
        Case 0:
        To test if the exception is throwed when pop() is called 
        and the stack is empty
        The function is wrapped so that its result is returned to 
        assertRaises() to be assessed.
        """
        S=Stack()
        with self.assertRaises(Exception): S.pop()
    
    def test_pop_1(self):
        """
        Case 1:
        To test if S.content is updated and the item formerly at the 
        top is returned, when pop() is called and the stack is not empty
        """
        S=Stack()
        S.push(10)
        #S=10
        self.assertEqual(S.pop(),10)
        self.assertTrue(np.isnan(S.content.head))
        #S is empty after pop()
        S.push(20)
        S.push(30)
        #S=30,20
        self.assertEqual(S.pop(), 30)
        #S=20
        self.assertEqual(S.content.head.key, 20)

    def test_peek_0(self):
        """
        Case 0:
        To test if the exception is throwed when peek() is called 
        and the stack is empty
        The funtion is wrapped so that its result is returned to 
        assertRaises() to be assessed.
        """
        S=Stack()
        with self.assertRaises(Exception): S.peek()

    def test_peek_1(self):
        """
        Case 1:
        To test if the item at the top (entering last) is returned, 
        but Stack.top is unchanged when pop() is called and the stack is not empty
        """
        S=Stack()
        S.push(10)
        S.push(20)
        #S=20, 10
        self.assertEqual(S.peek(),20)
        self.assertEqual(S.content.head.key,20)

    def test_stackEmpty_0(self):
        """
        Case 0:
        To test if "True" is returned when the stack is empty at initialisation 
        or after all items are popped out
        """
        S=Stack()
        self.assertTrue(S.stackEmpty())
        S.push(1)
        S.push(2)
        #S=2,1
        S.pop()
        #S=1
        S.pop()
        #S is empty
        self.assertTrue(S.stackEmpty())

    def test_stackEmpty_1(self):
        """
        Case 1:
        To test if "False" is returned when items are pushed to the Stack
        """
        S=Stack()
        S.push(1)
        #S=1
        self.assertFalse(S.stackEmpty())
        S.push(2)
        #S=2,1
        self.assertFalse(S.stackEmpty())

    def test_queue_init(self):
        """
        To test if the Stack.content is correctly initialised as a singly linked list
        """
        Q=Queue()
        self.assertTrue(isinstance(Q.content, singly_linked_list))

    def test_enqueue(self):
        """
        To test if an element is successfully added to the queue
        """
        Q=Queue()
        Q.enqueue(1)
        #Q=1
        self.assertEqual(Q.content.head.key, 1)
        self.assertTrue(np.isnan(Q.content.head.next))
        Q.enqueue(2)
        #Q=2,1
        self.assertEqual(Q.content.head.key, 2)
        self.assertEqual(Q.content.head.next.key, 1)
    
    def test_dequeue_0(self):
        """
        Case 0:
        To test if error is raised when the queue is empty
        """
        Q=Queue()
        #Q is empty
        with self.assertRaises(Exception): Q.dequeue()

    def test_dequeue_1(self):
        """
        Case 1:
        To test if the first added element is successfully removed from the queue
        This is the only element in the list
        """
        Q=Queue()
        Q.enqueue(1)
        #Q=1
        result=Q.dequeue()
        self.assertEqual(result, 1)
        self.assertTrue(np.isnan(Q.content.head))

    def test_dequeue_2(self):
        """
        Case 1:
        To test if the first added element is successfully removed from the queue
        """
        Q=Queue()
        Q.enqueue(1)
        Q.enqueue(2)
        Q.enqueue(3)
        #Q=3, 2, 1
        result=Q.dequeue()
        self.assertEqual(result, 1)
        self.assertEqual(Q.content.head.key, 3)
        self.assertEqual(Q.content.head.next.key, 2)
        self.assertTrue(np.isnan(Q.content.head.next.next))

if __name__ == '__main__':
    unittest.main()

