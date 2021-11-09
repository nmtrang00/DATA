#!/bin/python
import unittest

from numpy.lib.function_base import delete

"""
Python does not support built-in array; therefore, I used numpy.array instead.
insert(), delete(), and search() functions are included.
"""
class node():
    def __init__(self,key):
        self.key=key
        self.next=None

class singly_linked_list():
    def __init__(self):
        self.head=None

    def insert(self, newElement):
        """
        To "splice" a newItem onto the front of the linked list
        O(1)
        """
        new_node=node(newElement)
        if self.head!=None:
            new_node.next=self.head
        self.head=new_node
    
    def search(self, key):
        """
        To find the first element of key "key" in the list
        O(n), n is the number of element in the list
        """
        node_to_find=self.head
        node_index=0
        while node_to_find!=None:
            if node_to_find.key==key:
                return node_to_find, node_index
            node_to_find=node_to_find.next
            node_index+=1
        return None, -1

    def delete(self, key_to_remove):
        """
        To delete the first node with matching key in the list
        O(n)
        When we delete the first node, ie. case List.head.key == key_to_remove,
        list.delete_by_node() runs in constant time, Ω(1).
        """
        if self.head.key == key_to_remove:
            node_to_remove=self.head
            self.head=node_to_remove.next #=None
            node_to_remove.next=None
        else:
            node_prev=self.head
            node_to_remove=self.head.next
            while node_to_remove!=None:
                if node_to_remove.key==key_to_remove:
                    node_prev.next=node_to_remove.next
                    node_to_remove.next=None
                    return "Delete successfully"
                node_prev=node_to_remove
                node_to_remove=node_to_remove.next
            return "Node with matching key not found"
    
class TestSinglyLinkedListMethods(unittest.TestCase):
    def test_node_init(self):
        """
        To test if a node is initialised correctly
        """
        n=node(0)
        self.assertEqual(n.key, 0)
        self.assertTrue(n.next==None)
        
    def test_singly_linked_list_init(self):
        """
        To test if a singly linked list is initialised correctly
        """
        L=singly_linked_list()
        self.assertTrue(L.head==None)
    
    def test_list_insert_0(self):
        """
        Case 0:
        To test if an item is successful added to the front of the list
        when the list is initially empty (L.head==NIL)
        """
        L=singly_linked_list()
        L.insert(5)
        #L= 5
        self.assertEqual(L.head.key, 5)
        self.assertTrue(L.head.next==None)

    def test_list_insert_1(self):
        """
        Case 1:
        To test if an item is successful added to the front of the list
        when the list has already had at least an item (L.head!=NIL)
        """
        L=singly_linked_list()
        L.insert(5)
        L.insert(6)
        #L= 6, 5
        self.assertEqual(L.head.key, 6)
        self.assertEqual(L.head.next.key,5)
        self.assertTrue(L.head.next.next==None)
        
    def test_list_search_0(self):
        """
        Case 0:
        To test if None and index of -1 are returned when there is no node
        in the list with input "key"
        """
        L=singly_linked_list()
        found_node, found_node_index=L.search(4)
        #L is empty
        self.assertTrue(found_node==None)
        self.assertEqual(found_node_index,-1)
        L.insert(5)
        L.insert(6)
        #L=5, 6
        found_node_1, found_node_index_1=L.search(4)
        self.assertTrue(found_node_1==None)
        self.assertEqual(found_node_index_1,-1)
    
    def test_list_search_1(self):
        """
        Case 1:
        To test if the node with key "key" and its position in the list 
        are returned when there is a matching node in the list with input "key"
        """
        L=singly_linked_list()
        L.insert(7)
        L.insert(5)
        L.insert(6)
        L.insert(4)
        #L=4, 6, 5, 7
        found_node, found_node_index=L.search(4)
        self.assertEqual(found_node.key, 4)
        self.assertEqual(found_node_index,0)
        found_node_1, found_node_index_1=L.search(7)
        self.assertEqual(found_node_1.key, 7)
        self.assertEqual(found_node_index_1,3)

    def test_list_search_2(self):
        """
        Case 2:
        To test if the lastest added node with key "key" and its position in the list 
        are returned 
        """
        L=singly_linked_list()
        L.insert(5)
        L.insert(5)
        L.insert(6)
        L.insert(4)
        #L=4, 6, 5, 5
        found_node, found_node_index=L.search(5)
        self.assertEqual(found_node.key, 5)
        self.assertEqual(found_node_index,2)

    def test_delete_0(self):
        """
        Case 0:
        Test if the first node with matching key is successful deleted from the list when calling delete())
        This node is the only element in the list
        """
        L=singly_linked_list()
        L.insert(4)
        L.delete(4)
        self.assertTrue(L.head==None)

    def test_delete_1(self):
        """
        Case 1:
        To test if the first node is successful deleted from the list when calling delete()
        This node is not the first nor the last element of the list
        """
        L=singly_linked_list()
        L.insert(5)
        L.insert(7)
        L.insert(5)
        L.insert(6)
        #L= 6, 5, 7, 5
        log=L.delete(5)
        #L_after_deletion= 6, 7, 5
        self.assertEqual(log,  "Delete successfully")
        self.assertEqual(L.head.key, 6)
        self.assertEqual(L.head.next.key, 7)
        self.assertEqual(L.head.next.next.key, 5)
        self.assertTrue(L.head.next.next.next==None)

    def test_delete_2(self):
        """
        Case 2:
        To test if the first node is successful deleted from the list when calling delete()
        This node is the last element of the list
        """
        L=singly_linked_list()
        L.insert(4)
        L.insert(7)
        L.insert(5)
        L.insert(6)
        #L= 6, 5, 7, 4
        log=L.delete(4)
        #L_after_deletion= 6, 5, 7
        self.assertEqual(log,  "Delete successfully")
        self.assertEqual(L.head.key, 6)
        self.assertEqual(L.head.next.key, 5)
        self.assertEqual(L.head.next.next.key, 7)
        self.assertTrue(L.head.next.next.next==None)

    def test_delete_3(self):
        """
        Case 3:
        To test if the correct log is returned when calling delete().
        The input key doesn't exist in the list.
        """
        L=singly_linked_list()
        L.insert(5)
        L.insert(7)
        L.insert(5)
        L.insert(6)
        #L= 6, 5, 7, 5
        log=L.delete(4)
        #L_after_deletion= 6, 5, 7, 5
        self.assertEqual(log, "Node with matching key not found")

if __name__ == '__main__':
    unittest.main()

