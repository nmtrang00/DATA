#!/bin/python

import unittest
from ex3_binary_tree import node, binary_tree

class binary_search_tree(binary_tree):
    """
    The left side of a node contains all nodes with key smaller than its key
    The right side of a node contains all nodes with key no smaller than its key
    """
    def __init__(self):
        binary_tree.__init__(self)

    def insert(self, newKey):
        """
        To add to a node with key value of "newKey" to the bst
        n=(2**h)-1 <=> h = log2(n + 1)
        O(tree_height)=O(log(n))
        """
        if self.root == None:
            self.set_root(newKey)
        else:
            parent=None #Use to store the parent node with child "None" right before the loop ends
            node_to_check=self.root
            while node_to_check!=None:
                parent=node_to_check
                if newKey < node_to_check.key:
                    node_to_check=node_to_check.left
                else:
                    node_to_check=node_to_check.right
            if newKey < parent.key:
                self.set_left_child(parent, node(newKey))
            else:
                self.set_right_child(parent, node(newKey))

    def inOrder(self, node_to_check):
        """
        To traverse the child nodes of the "node_to_check" and print the node_to check in increasing order
        O(n): Each node from "node_to_check" and below is visited once
        Eg.
        (1)---(2)   
            |
            |_(0)
        result: 0 1 2
        """
        if node_to_check!= None:
            self.inOrder(node_to_check.left)
            print(node_to_check.key, end=" ")
            self.inOrder(node_to_check.right)

    def printInOrder(self):
        """
        To call inOrder recursively starting from the root of the bst
        O(n): Each node in the tree is visited once
        """
        self.inOrder(self.root)

class TestBinarySearchTreeMethods(unittest.TestCase):
    def test_bst_init(self):
        """
        To test if a bst is initialised successfully
        """
        bst=binary_search_tree()
        self.assertIsInstance(bst, binary_tree)

    def test_insert_0(self):
        """
        To test if a node is added to the bst successfully
        The bst is currently empty
        """
        bst=binary_search_tree()
        self.assertIsNone(bst.root)
        bst.insert(15)
        self.assertEqual(bst.root.key, 15)
    
    def test_insert_1(self):
        """
        To test if a node is added to the bst successfully
        The bst has already had at least a node
        eg.
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
        self.assertEqual(bst.root.left.key, 6)
        bst.insert(7)
        self.assertEqual(bst.root.left.right.key, 7)
        bst.insert(18)
        self.assertEqual(bst.root.right.key, 18)
        bst.insert(17)
        self.assertEqual(bst.root.right.left.key, 17)

    def test_print_in_order(self):
        """
        To test if the nodes'keys are printed in increasing order
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
        bst.printInOrder()

if __name__ == '__main__':
    unittest.main()