#!/bin/python

from logging import root
import unittest
import math
import numpy as np
from doubly_linked_list import doubly_linked_list
"""
Eg.
(0)---(2)---(6)
     |     |
     |     |_(5)
     |
     |_(1)---(4)
            |
            |_(3)
"""
class node():
    def __init__(self, key):
        self.key=key
        self.parent=None
        self.left=None
        self.right=None

class binary_tree():
    def __init__(self):
        self.root=None

    def set_root(self, key):
        """
        To set a node as the root of the tree
        O(1)
        """
        self.root=node(key)

    def set_left_child(self, parent, child):
        """
        To add a node as the left child of another node
        O(1)
        """
        parent.left=child
        child.parent=parent
    
    def set_right_child(self, parent, child):
        """
        To add a node as the right child of another node
        O(1)
        """
        parent.right=child
        child.parent=parent
    
class TestBinaryTreeMethods(unittest.TestCase):
    def test_node_init(self):
        """
        To test if a node is initialised correctly
        """
        n=node(1)
        self.assertEqual(n.key, 1)
        self.assertIsNone(n.parent)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_bt_init(self):
        """
        To test if a binary tree is initialised correctly
        """
        BT=binary_tree()
        self.assertIsNone(BT.root)

    def test_set_root(self):
        """
        To test if the root of a tree is set correctly
        """
        BT=binary_tree()
        BT.set_root(0)
        self.assertEqual(BT.root.key, 0)
        self.assertIsNone(BT.root.parent)
        self.assertIsNone(BT.root.left)
        self.assertIsNone(BT.root.right)

    def test_set_left_child_0(self):
        """
        To test if a child node is successfully added to the left of a parent node
        The child node is a completely new node with no child
        """
        BT=binary_tree()
        BT.set_root(0)
        child_node=node(1)
        BT.set_left_child(BT.root, child_node)
        self.assertIsInstance(BT.root.left, node)
        self.assertEqual(BT.root.left.key, 1)
        self.assertIsInstance(child_node.parent, node)
        self.assertEqual(child_node.parent.key, 0)

    def test_set_right_child_0(self):
        """
        To test if a child node is successfully added to the right of a parent node
        The child node is a completely new node with no child
        """
        BT=binary_tree()
        BT.set_root(0)
        child_node=node(1)
        BT.set_right_child(BT.root, child_node)
        self.assertIsInstance(BT.root.right, node)
        self.assertEqual(BT.root.right.key, 1)
        self.assertIsInstance(child_node.parent, node)
        self.assertEqual(child_node.parent.key, 0)

    def test_set_left_child_1(self):
        """
        To test if a child node is successfully added to the left of a parent node
        The child node also has childs
        Eg.
        (0)---NIL   
            |
            |_(1)---(3)
                    |
                    |_(2)
        """
        BT=binary_tree()
        BT.set_root(0)
        child_node=node(1)
        child_node.left=node(2)
        child_node.right=node(3)
        BT.set_left_child(BT.root, child_node)
        self.assertIsInstance(BT.root.left, node)
        self.assertEqual(BT.root.left.key, 1)
        self.assertIsInstance(child_node.parent, node)
        self.assertEqual(child_node.parent.key, 0)
        self.assertEqual(BT.root.left.left.key, 2)
        self.assertEqual(BT.root.left.right.key, 3)

    def test_set_right_child_1(self):
        """
        To test if a child node is successfully added to the right of a parent node
        The child node also has childs
        Eg.
        (0)---(1)---(3)
            |     |
            |     |_(2)
            |
            |_NIL
        """
        BT=binary_tree()
        BT.set_root(0)
        child_node=node(1)
        child_node.left=node(2)
        child_node.right=node(3)
        BT.set_right_child(BT.root, child_node)
        self.assertIsInstance(BT.root.right, node)
        self.assertEqual(BT.root.right.key, 1)
        self.assertIsInstance(child_node.parent, node)
        self.assertEqual(child_node.parent.key, 0)
        self.assertEqual(BT.root.right.left.key, 2)
        self.assertEqual(BT.root.right.right.key, 3)

if __name__ == '__main__':
    unittest.main()