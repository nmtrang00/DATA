#!/bin/python

import unittest
import math
import time
from ex4_binary_search_tree import node, binary_search_tree
def iterative_tree_search(bst, key):
    """
    To check if there exists a node with matching key in bst
    O(height)=O(log(n))
    """
    node_to_check=bst.root
    while node_to_check!=None and node_to_check.key!=key:
        if key < node_to_check.key:
            node_to_check=node_to_check.left
        else:
            node_to_check=node_to_check.right
    if node_to_check == None:
        return False
    else:
        return True

class TestTreeSearch(unittest.TestCase):
    def test_iterative_tree_search_0(self):
        """
        To test if False is returned when there is no node in bst with matching key
        eg. 6 7 15 17 18
        (15)---(18)---NIL
              |      |
              |      |_(17)
              |
              |_(6)---(7)
                      |
                      |_NIL
        """
        bst=binary_search_tree()
        bst.insert(15)
        bst.insert(6)
        bst.insert(7)
        bst.insert(18)
        bst.insert(17)
        self.assertFalse(iterative_tree_search(bst, 10))    

    def test_iterative_tree_search_1(self):
        """
        To test if True is returned when there is a node in bst with matching key
        eg. 6 7 15 17 18
        (15)---(18)---NIL
              |      |
              |      |_(17)
              |
              |_(6)---(7)
                      |
                      |_NIL
        """
        bst=binary_search_tree()
        bst.insert(15)
        bst.insert(6)
        bst.insert(7)
        bst.insert(18)
        bst.insert(17)
        time_start=time.time()
        self.assertTrue(iterative_tree_search(bst, 18))    
        print(time.time()-time_start)

if __name__ == '__main__':
    unittest.main()


# def bst_tree_search(bst, key):
#     """
#     To check if there exists a node with matching key in bst
#     """
#     current_node=bst.root
#     found_node=tree_search(current_node, key)
#     if found_node==None:
#         return False
#     else:
#         return True

# def tree_search(node_to_check, key):
#     """
#     To check if there exists a node with matching key below node_to_check
#     """
#     if node_to_check==None or node_to_check.key==key:
#         return node_to_check
#     if key < node_to_check.key:
#         return tree_search(node_to_check.left, key)
#     else:
#         return tree_search(node_to_check.right, key)

#Test
# def test_tree_search_0(self):
#         """
#         To test if None is returned when the node_to_check is NIL
#         Eg.
#         (1)---(2)   
#             |
#             |_NIL
#         """
#         node_1=node(1)
#         node_1.right=node(2)
#         self.assertIsNone(tree_search(node_1.left, 1))
    
#     def test_tree_search_1(self):
#         """
#         To test if the node with matching key is returned 
#         Eg.
#         (1)---(2)   
#             |
#             |_NIL
#         """
#         node_1=node(1)
#         node_2=node(2)
#         node_1.right=node_2
#         node_2.parent=node_1
#         found_node=tree_search(node_1, 2)
#         self.assertEqual(found_node.key, 2)
#         self.assertEqual(found_node.parent.key, 1)

#     def test_bst_tree_search_0(self):
#         """
#         To test if False is returned when there is no node in bst with matching key
#         eg. 6 7 15 17 18
#         (15)---(18)---NIL
#               |      |
#               |      |_(17)
#               |
#               |_(6)---(7)
#                       |
#                       |_NIL
#         """
#         bst=binary_search_tree()
#         bst.insert(15)
#         bst.insert(6)
#         bst.insert(7)
#         bst.insert(18)
#         bst.insert(17)
#         self.assertFalse(bst_tree_search(bst, 10))

#     def test_bst_tree_search_1(self):
#         """
#         To test if True is returned when there is a node in bst with matching key
#         eg. 6 7 15 17 18
#         (15)---(18)---NIL
#               |      |
#               |      |_(17)
#               |
#               |_(6)---(7)
#                       |
#                       |_NIL
#         """
#         bst=binary_search_tree()
#         bst.insert(15)
#         bst.insert(6)
#         bst.insert(7)
#         bst.insert(18)
#         bst.insert(17)
#         self.assertTrue(bst_tree_search(bst, 18))