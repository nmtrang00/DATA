#!/bin/python
import numpy as np
import unittest

from doubly_linked_list import node, doubly_linked_list

class item():
    def __init__(self, key, value):
        node.__init__(self, key)
        self.value=value

class hash_table():
    def __init__(self, hash_function, number_of_keys):
        self.hash_function=hash_function
        # self.content=np.array([doubly_linked_list()]*number_of_keys) 
        # => Error: instances created point to the same object=> When insert(), the item is inserted to all instances
        self.content=np.array([None]*number_of_keys)
        
    def hash_insert(self, newItem):
        """
        To add a new item to the hash table, assuming that the item.key has not been already in the table
        O(1): double_linked_list.insert() works in O(1)
        (Assume that hash_ function works in O(1))
        """
        hashed_value=self.hash_function(newItem.key)
        if self.content[hashed_value]==None:
            self.content[hashed_value]=doubly_linked_list()
        self.content[hashed_value].insert(newItem)

    def hash_insert_with_check_key(self, newItem):
        """
        To add a new item to the hash table, if the key exists in the hash table, its value is replaced with new value
        O(n): double_linked_list.insert() works in O(1), but the loop makes the funciton works in O(n)
        (Assume that hash_ function works in O(1))
        """
        hashed_value=self.hash_function(newItem.key)
        #No item in the list of that hashed_value
        if self.content[hashed_value]==None: 
            self.content[hashed_value]=doubly_linked_list()
            self.content[hashed_value].insert(newItem)
            return 0
        #At least an item in the list of that hashed_value
        node_to_find=self.content[hashed_value].head.next
        while node_to_find!=None:
            if node_to_find.key==newItem.key:
                node_to_find.value=newItem.value
                return 1 
            node_to_find=node_to_find.next
        self.content[hashed_value].insert(newItem)
        return 2

    def hash_search(self, key):
        """
        To find the value of an item with a given key
        O(n): double_linked_list.search() works in O(n)
        (Assume that hash_ function works in O(1))
        """
        hashed_value=self.hash_function(key)
        if self.content[hashed_value]==None:
            return None
        return self.content[hashed_value].search(key)[0]

    def hash_delete(self, item_to_remove):
        """
        To delete an item from the hash table
        O(1): double_linked_list.delete() works in O(1)
        (Assume that hash_ function works in O(1))
        """
        self.content[self.hash_function(item_to_remove.key)].delete(item_to_remove)

class TestHashTableMethods(unittest.TestCase):
    def test_item_init(self):
        """
        To test if an item is initialised correctly
        """
        n=item("key",2)
        self.assertEqual(n.key, "key")
        self.assertEqual(n.value, 2)
        self.assertEqual(n.next, None)
        self.assertEqual(n.prev, None)

    def test_hash_table_init(self):
        """
        To test if a hash table is initialised correctly
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        self.assertEqual(H.hash_function(1), 1)
        self.assertEqual(H.hash_function(6), 0)
        self.assertEqual(H.content.shape[0], 3)
        self.assertIsNone(H.content[0])


    def test_hash_insert(self):
        """
        To test if a new item is successfully added to the hash table
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        H.hash_insert(item(11,1)) #11%3=2 => H[2]=item(11,1)
        self.assertIsNone(H.content[0])
        self.assertIsNone(H.content[1])
        self.assertEqual(H.content[2].head.next.key,11)
        self.assertEqual(H.content[2].head.next.value,1)
        self.assertIsNone(H.content[2].head.next.prev.key) #H.content[2].head.next.prev=H.content[2].head
        self.assertIsNone(H.content[2].head.next.next)
        H.hash_insert(item(17,3)) #17%3=2 => H[2]=item(17,3), item(11,1)
        self.assertEqual(H.content[2].head.next.key,17)
        self.assertEqual(H.content[2].head.next.value,3)
        self.assertEqual(H.content[2].head.next.next.key,11)
        self.assertEqual(H.content[2].head.next.next.value,1)
    

    def test_hash_insert_with_check_key_0(self):
        """
        To test if a new item is successfully added to the hash table
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        return_code=H.hash_insert_with_check_key(item(11,1)) #11%3=2 => H[2]=item(11,1)
        self.assertEqual(return_code, 0)
        self.assertIsNone(H.content[0])
        self.assertIsNone(H.content[1])
        self.assertEqual(H.content[2].head.next.key,11)
        self.assertEqual(H.content[2].head.next.value,1)
        self.assertIsNone(H.content[2].head.next.prev.key) #H.content[2].head.next.prev=H.content[2].head
        self.assertIsNone(H.content[2].head.next.next)
        return_code_1=H.hash_insert_with_check_key(item(17,3)) #17%3=2 => H[2]=item(17,3), item(11,1)
        self.assertEqual(return_code_1, 2)
        self.assertEqual(H.content[2].head.next.key,17)
        self.assertEqual(H.content[2].head.next.value,3)
        self.assertEqual(H.content[2].head.next.next.key,11)
        self.assertEqual(H.content[2].head.next.next.value,1)
    
    def test_hash_insert_with_check_key_1(self):
        """
        To test if the value of an item is replaced when a new item with the same key is added to the table
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        H.hash_insert_with_check_key(item(11,1)) #11%3=2 => H[2]=item(11,1)
        H.hash_insert_with_check_key(item(17,3)) #17%3=2 => H[2]=item(17,3), item(11,1)
        return_code=H.hash_insert_with_check_key(item(11,2)) #H[2]=item(17,3), item(11,2)
        self.assertEqual(return_code, 1)
        self.assertEqual(H.content[2].head.next.next.key,11)
        self.assertEqual(H.content[2].head.next.next.value,2)

    def test_hash_search_0(self):
        """
        To test if None is returned when there is no item
        in the hash table with matching "key"
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        found_item= H.hash_search(0)
        self.assertIsNone(found_item)
        H.hash_insert(item(11,1)) #11%3=2 => H[2]=item(11,1)
        found_item_1= H.hash_search(0)
        self.assertIsNone(found_item_1)

    def test_hash_search_1(self):
        """
        To test if the item with matching key and its index are returned when calling hash_search()
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        H.hash_insert(item(11,1)) #11%3=2 => H[2]=item(11,1)
        H.hash_insert(item(17,3)) #17%3=2 => H[2]=item(17,3), item(11,1)
        H.hash_insert(item(22,2)) #22%3=1 => H[1]=item(22,1)
        found_item= H.hash_search(11)
        self.assertEqual(found_item.key, 11)
        self.assertEqual(found_item.value, 1)

    def test_hash_delete(self):
        """
        To test if an item is successfully removed from the table
        """
        def test_function(x):
            return x%3
        H=hash_table(test_function,3) #Modulo p=3, so there are only 3 slots at max in the table
        item_to_delete=item(17,2)
        H.hash_insert(item(11,1)) #11%3=2 => H[2]=item(11,1)
        H.hash_insert(item_to_delete) #17%3=2 => H[2]=item(17,3), item(11,1)
        H.hash_insert(item(23,3)) #23%3=2 => H[2]=item(23,3), item(17,3), item(11,1)
        H.hash_delete(item_to_delete) #H[2]_after_delettion = item(23,3), item(11,1)
        self.assertEqual(H.content[2].head.next.key,23)
        self.assertEqual(H.content[2].head.next.value,3)
        self.assertEqual(H.content[2].head.next.next.key,11) 
        self.assertEqual(H.content[2].head.next.next.value,1)
        self.assertIsNone(H.content[2].head.next.next.next) 

if __name__ == '__main__':
    unittest.main()