#!/bin/python
import unittest

from doubly_linked_list import node, doubly_linked_list
from ex1_hash_table import item, hash_table

class dictionary:
    def __init__(self, items=[]):
        self.hash_table=hash_table(self.hash_function_division, 3)
        if len(items) > 1: 
            for item in items:
                self.dict_insert(item)

    def hash_function_division(self,x):
        """
        Just an arbitary modulo hash function to test the class. 
        For more detailed analysis of hash function, please check ex2_test_hash_function.
        """
        return x%3      

    def dict_insert(self, newItem):
        """
        To add a new item to the dictionary
        O(n): hash_insert_with_check_key() works in O(n)
        """
        self.hash_table.hash_insert_with_check_key(newItem)

    def dict_search(self, key):
        """
        To search for an item with matching key in the dictionary
        O(n): hash_search() works in O(n)
        """
        return self.hash_table.hash_search(key)

    def dict_delete(self, item_to_remove):
        """
        To remove an item out of the list
        O(1): hash_delete() works in O(1)
        """
        return self.hash_table.hash_delete(item_to_remove)


class TestDictionaryMethods(unittest.TestCase):

    def test_dictionary_init(self):
        """
        To test if a dictionary is initialised correctly
        """
        D=dictionary() 
        self.assertIsInstance(D.hash_table, hash_table)
        self.assertEqual(D.hash_table.content.shape[0], 3)
        self.assertIsNone(D.hash_table.content[0])

    def test_dict_insert_1(self):
        """
        To test if a new item is successfully added to the dictionary
        """
        D=dictionary()
        D.dict_insert(item(11,0)) #11%3=2 => D[2]=item(11,0)
        self.assertEqual(D.hash_table.content[2].head.next.key,11)
        self.assertEqual(D.hash_table.content[2].head.next.value,0)
        self.assertIsNone(D.hash_table.content[2].head.next.prev.key) #D.hash_table.content[2].head.next.prev=D.content[2].head
        self.assertIsNone(D.hash_table.content[2].head.next.next)
        D.dict_insert(item(17,1)) #17%3=2 => D[2]=item(17,1), item(11,0)
        self.assertEqual(D.hash_table.content[2].head.next.key,17)
        self.assertEqual(D.hash_table.content[2].head.next.value,1)
        self.assertEqual(D.hash_table.content[2].head.next.next.key,11)
        self.assertEqual(D.hash_table.content[2].head.next.next.value,0)
    
    def test_dict_insert_2(self):
        """
        To test if the value of an item is replaced when a new item with the same key is added to the dict
        """
        D=dictionary()
        D.dict_insert(item(11,0)) #11%3=2 => D[2]=item(11,0)
        D.dict_insert(item(11,1)) #D[2]= item(11,1)
        self.assertEqual(D.hash_table.content[2].head.next.key,11)
        self.assertEqual(D.hash_table.content[2].head.next.value,1)

    def test_dict_init_with_args(self):
        """
        To test if a dictionary is initialised correctly
        """
        D=dictionary([item(11,0), item(17,1)])
        self.assertIsInstance(D.hash_table, hash_table)
        self.assertEqual(D.hash_table.content.shape[0], 3)
        self.assertIsNone(D.hash_table.content[0])
        self.assertEqual(D.hash_table.content[2].head.next.key,17)
        self.assertEqual(D.hash_table.content[2].head.next.value,1)
        self.assertEqual(D.hash_table.content[2].head.next.next.key,11)
        self.assertEqual(D.hash_table.content[2].head.next.next.value,0)

    def test_dict_search_0(self):
        """
        To test if None is returned when there is no item
        in the hash table with matching "key"
        """
        D=dictionary()
        found_item= D.dict_search(0)
        self.assertIsNone(found_item)
        D.dict_insert(item(11,1))
        found_item_1= D.dict_search(0)
        self.assertIsNone(found_item_1)

    def test_dict_search_1(self):
        """
        To test if the item with matching key and its index are returned when calling dict_search()
        """
        D=dictionary([item(11,0), item(17,1), item(11,2)])
        found_item= D.dict_search(11)
        self.assertEqual(found_item.key, 11)
        self.assertEqual(found_item.value, 2)

    def test_dict_delete(self):
        """
        To test if an item is successfully removed from the dict
        """
        item_to_delete=item(17,1)
        D=dictionary([item(11,0), item_to_delete]) #11%3=17%3=2
        D.dict_delete(item_to_delete)
        self.assertEqual(D.hash_table.content[2].head.next.key,11)
        self.assertEqual(D.hash_table.content[2].head.next.value,0)

if __name__ == '__main__':
    unittest.main()