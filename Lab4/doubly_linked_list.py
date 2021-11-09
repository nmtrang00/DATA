#!/bin/python
import unittest


"""
Python does not support built-in array; therefore, I used numpy.array instead.
insert(), delete(), and search() functions are included.
"""
class node():
    def __init__(self,key):
        self.key=key
        self.next=None
        self.prev=None

class doubly_linked_list():
    def __init__(self):
        self.head=node(None) #Head of the list is a node with key of None, supporting insert() function

    def insert(self, new_node):
        """
        To "splice" a new node onto the front of the linked list
        O(1)
        """
        new_node.next=self.head.next
        if self.head.next!=None:
            self.head.next.prev=new_node
        self.head.next=new_node
        new_node.prev=self.head

    def search(self, key):
        """
        To find the first element of key "key" in the list
        O(n), n is the number of element in the list
        """
        node_to_find=self.head.next
        node_index=0
        while node_to_find!=None:
            if node_to_find.key==key:
                return node_to_find, node_index
            node_to_find=node_to_find.next
            node_index+=1
        return None, -1

    def delete(self, node_to_remove):
        """
        To delete a node in the list
        O(1)
        """
        node_to_remove.prev.next=node_to_remove.next
        if node_to_remove.next != None:
            node_to_remove.next.prev=node_to_remove.prev
        node_to_remove.next=None
        node_to_remove.prev=None
        

class TestDoublyLinkedListMethods(unittest.TestCase):
    def test_node_init(self):
        """
        To test if a node is initialised correctly
        """
        n=node(0)
        self.assertEqual(n.key, 0)
        self.assertEqual(n.next, None)
        self.assertEqual(n.prev, None)
        
    def test_doubly_linked_list_init(self):
        """
        To test if a singly linked list is initialised correctly
        """
        L=doubly_linked_list()
        self.assertTrue(isinstance(L.head,node))
        self.assertEqual(L.head.key,None)
        self.assertEqual(L.head.prev,None)
        self.assertEqual(L.head.next,None)

    def test_list_insert_0(self):
        """
        Case 0:
        To test if an item is successful added to the front of the list
        when the list is initially empty (L.head==NIL)
        """
        L=doubly_linked_list()
        L.insert(node(5))
        #L= 5
        self.assertEqual(L.head.next.key, 5)
        self.assertEqual(L.head.next.next,None)
        self.assertEqual(L.head.next.prev, L.head)

    def test_list_insert_1(self):
        """
        Case 1:
        To test if an item is successful added to the front of the list
        when the list has already had at least an item (L.head!=NIL)
        """
        L=doubly_linked_list()
        L.insert(node(5))
        L.insert(node(6))
        #L= 6, 5
        self.assertEqual(L.head.next.key, 6)
        self.assertEqual(L.head.next.prev, L.head)
        self.assertEqual(L.head.next.next.key,5)
        self.assertEqual(L.head.next.next.next,None)
       
    def test_list_search_0(self):
        """
        Case 0:
        To test if None and index of -1 are returned when there is no node
        in the list with input "key"
        """
        L=doubly_linked_list()
        found_node, found_node_index=L.search(4)
        #L is empty
        self.assertEqual(found_node, None)
        self.assertEqual(found_node_index,-1)
        L.insert(node(5))
        L.insert(node(6))
        #L=5, 6
        found_node_1, found_node_index_1=L.search(4)
        self.assertEqual(found_node_1, None)
        self.assertEqual(found_node_index_1,-1)
    
    def test_list_search_1(self):
        """
        Case 1:
        To test if the node with key "key" and its position in the list 
        are returned when there is a matching node in the list with input "key"
        """
        L=doubly_linked_list()
        L.insert(node(7))
        L.insert(node(5))
        L.insert(node(6))
        L.insert(node(4))
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
        To test if the 1st node with key "key" and its position in the list 
        are returned 
        """
        L=doubly_linked_list()
        L.insert(node(5))
        L.insert(node(5))
        L.insert(node(6))
        L.insert(node(4))
        #L=4, 6, 5, 5
        found_node, found_node_index=L.search(5)
        self.assertEqual(found_node.key, 5)
        self.assertEqual(found_node_index,2)

    def test_delete_0(self):
        """
        Case 0:
        To test if the lastest added node is successful deleted from the list when calling delete()
        This node is the first element of the list
        """
        L=doubly_linked_list()
        L.insert(node(5))
        L.insert(node(7))
        L.insert(node(5))
        L.insert(node(6))
        #L= 6, 5, 7, 5
        L.delete(L.search(6)[0])
        #L_after_deletion= 5, 7, 5
        self.assertEqual(L.head.next.key, 5)
        self.assertEqual(L.head.next.next.key, 7)
        self.assertEqual(L.head.next.next.next.key, 5)
        self.assertEqual(L.head.next.next.next.next,None)

    def test_delete_2(self):
        """
        Case 2:
        To test if the first node is successful deleted from the list when calling delete_by_node()
        This node is not the first nor the last element of the list
        """
        L=doubly_linked_list()
        L.insert(node(5))
        L.insert(node(7))
        L.insert(node(5))
        L.insert(node(6))
        #L= 6, 5, 7, 5
        L.delete(L.search(5)[0])
        #L_after_deletion= 6, 7, 5
        self.assertEqual(L.head.next.key, 6)
        self.assertEqual(L.head.next.next.key, 7)
        self.assertEqual(L.head.next.next.next.key, 5)
        self.assertEqual(L.head.next.next.next.next, None)

    def test_delete_3(self):
        """
        Case 3:
        To test if the first node is successful deleted from the list when calling delete_by_node()
        This node is the last element of the list
        """
        L=doubly_linked_list()
        L.insert(node(4))
        L.insert(node(7))
        L.insert(node(5))
        L.insert(node(6))
        #L= 6, 5, 7, 4
        L.delete(L.search(4)[0])
        #L_after_deletion= 6, 5, 7
        self.assertEqual(L.head.next.key, 6)
        self.assertEqual(L.head.next.next.key, 5)
        self.assertEqual(L.head.next.next.next.key, 7)
        self.assertEqual(L.head.next.next.next.next, None)


if __name__ == '__main__':
    unittest.main()
