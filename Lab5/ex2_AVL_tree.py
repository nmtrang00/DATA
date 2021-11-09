#!/bin/python

import unittest
import sys

sys.path.append('/Users/trangnguyen/Documents/Study/DATA/Lab4')
from ex3_binary_tree import node, binary_tree
from ex4_binary_search_tree import binary_search_tree
from ex1_bst_rotate import bst_rotate

class AVL_node(node):
    def __init__(self, key):
        node.__init__(self, key)
        self.height=1

class AVL_tree(bst_rotate):

    def __init__(self):
        bst_rotate.__init__(self)

    def get_height_0(self, node_to_check):
        """
        To get height of a node in the tree
        O(h)=O(log(n))
        """
        if node_to_check==None:
            return 0
        elif node_to_check.left==None and node_to_check.right==None:
            return 1
        else:
            return 1+max(self.get_height_0(node_to_check.left), self.get_height_0(node_to_check.right))

    def balance_0(self, node_to_balance):
        """
        To obtain the optimal height difference (<=1) of a node left and right child, 
        by rotating it and its child.
        
        Condition: The difference of height on the input node's left and right child is smaller or equal to 2, 
        which is maintained by the AVL_insert(). Plus, the subtree rooted at left and right childs are already balanced
        
        O(log(n)): Both rotate_right() and rotate_left() run in O(1), but get_height works in O(log(n))
        
        See more illustrations in DATA-Lab5.pdf
        """
        h_leftChild=self.get_height_0(node_to_balance.left)
        h_rightChild=self.get_height_0(node_to_balance.right)
        if abs(h_leftChild-h_rightChild)>2: #Case 0
            return -1
        if h_leftChild > h_rightChild + 1: #Case 1
            if self.get_height_0(node_to_balance.left.left) < self.get_height_0(node_to_balance.left.right):
                self.rotate_left(node_to_balance.left)
            self.rotate_right(node_to_balance)
        elif h_rightChild > h_leftChild + 1: #Case 2
            if self.get_height_0(node_to_balance.right.right) < self.get_height_0(node_to_balance.right.left):
                self.rotate_right(node_to_balance.right)
            self.rotate_left(node_to_balance)

    def get_height(self, node_to_check):
        """
        To get height of a node in the tree
        O(1)
        """
        if node_to_check==None:
            return 0
        else:
            return node_to_check.height

    def balance(self, node_to_balance):
        """
        To obtain the optimal height difference (<=1) of a node left and right child, 
        by rotating it and its child.
        
        Condition: The difference of height on the input node's left and right child is smaller or equal to 2, 
        which is maintained by the AVL_insert(). Plus, the subtree rooted at left and right childs are already balanced
        
        O(1): Both rotate_right() and rotate_left() run in O(1)
        
        See more illustrations in DATA-Lab5.pdf
        """
        h_leftChild=self.get_height(node_to_balance.left)
        h_rightChild=self.get_height(node_to_balance.right)
        if abs(h_leftChild-h_rightChild)>2: #Case 0
            return -1
        if h_leftChild > h_rightChild + 1: #Case 1
            if self.get_height(node_to_balance.left.left) < self.get_height(node_to_balance.left.right):
                self.rotate_left(node_to_balance.left)
            self.rotate_right(node_to_balance)
        elif h_rightChild > h_leftChild + 1: #Case 2
            if self.get_height(node_to_balance.right.right) < self.get_height(node_to_balance.right.left):
                self.rotate_right(node_to_balance.right)
            self.rotate_left(node_to_balance)

    def balance_recursive(self, node_to_balance):
        """
        With the assumption of balanced subtree, we need a function to balance the parent tree after the subtree is reordered 
        O(log(n)): balance() works in O(log(n))
        """
        p=node_to_balance.parent
        self.balance(node_to_balance)
        #Update height
        node_to_balance.height=1+max(self.get_height(node_to_balance.left), self.get_height(node_to_balance.right))
        #Check if we reach the root => Stop the recursive
        if p !=None:
            return self.balance_recursive(p)
        else:
            return 1

    def insert_without_balancing_height_update(self, newKey):
        """
        Modified from the insert of BST to use AVL_node as the type of node in tree, the algorithm is the same
        O(h)=O(log(n))
        """
        new_node=AVL_node(newKey)
        if self.root == None:
            self.root=new_node
            return 0
        parent=None #Use to store the parent node with child "None" right before the loop ends
        node_to_check=self.root
        while node_to_check!=None:
            parent=node_to_check
            if newKey < node_to_check.key:
                node_to_check=node_to_check.left
            else:
                node_to_check=node_to_check.right
        if newKey < parent.key:
            self.set_left_child(parent, new_node)
        else:
            self.set_right_child(parent, new_node)
        return new_node

    def AVL_insert(self, newKey):
        """
        To add to a node with key value of "newKey" to the bst
        O(log(n)): insert_without_balancing_height_update() runs in O(log(n))
        """
        #Insert
        new_node=self.insert_without_balancing_height_update(newKey)
        if new_node == 0:
            return 0
        #Balance
        return self.balance_recursive(new_node)

class TestAVLMethods(unittest.TestCase):
    def test_avl_tree_init(self):
        """
        To test if an avl is initialised successfully
        """
        avl=AVL_tree()
        self.assertIsInstance(avl, binary_search_tree)

    def test_get_height_0(self):
        """
        To test if the 0 is returned as height if the input is not a node
        (15)---NIL  
              |
              |_(6)
        """
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(6)
        self.assertEqual(avl.get_height_0(avl.root.right),0)
    
    def test_get_height_1(self):
        """
        To test if the 1 is returned as height if the node is a leaf
        (15)---NIL  
              |
              |_(6)
        """
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(6)
        self.assertEqual(avl.get_height_0(avl.root.left),1)

    def test_get_height_2(self):
        """
        To test if the height is returned correctly when the node is the root of the tree
        (15)---NIL  
              |
              |_(6)
        """
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(6)
        self.assertEqual(avl.get_height_0(avl.root),2)

    def test_get_height_3(self):
        """
        To test if the height is returned correctly when the node is either a root or a leaf of the tree
        (6)---(7)---(13)  
             |     |
             |     |_NIL
             |
             |_(3)
        """
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(6)
        avl.insert_without_balancing_height_update(7)
        avl.insert_without_balancing_height_update(3)
        avl.insert_without_balancing_height_update(13)
        self.assertEqual(avl.get_height_0(avl.root.right),2)

    def test_balance_0(self):
        """
        Case0: To test if -1 is returned when the diff in height of 2 childs is greater than 2
        (6)---(7)---(13)---(15)
             |     |      |
             |     |      |_(10)
             |     |
             |     |_NIL
             |
             |_NIL
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(6)
        avl.insert_without_balancing_height_update(7)
        avl.insert_without_balancing_height_update(13)
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(10)
        self.assertEqual(avl.balance_0(avl.root),-1)
    
    def test_balance_1_1(self):
        """
        Case 1.1: The node to balance's left child has greater length and left child's childs have equal height
        (10)---NIL
              |
              |_(3)---(5)
                     |
                     |_(0) 
        Rebalance:
        (3)---(10)---NIL
             |      |
             |      |_(5)
             |
             |_(0)
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(3)
        avl.insert_without_balancing_height_update(5)
        avl.insert_without_balancing_height_update(0)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 3)
        self.assertEqual(avl.root.left.key, 0)
        self.assertEqual(avl.root.right.key, 10)
        self.assertEqual(avl.root.right.left.key, 5)
        self.assertIsNone(avl.root.right.right)
    
    def test_balance_1_2(self):
        """
        Case 1.2: The node to balance's left child has greater length and left child' s left child has greater height
        (10)---NIL
              |
              |_(3)---NIL
                     |
                     |_(0) 
        Rebalance:
        (3)---(10)---NIL
             |      |
             |      |_NIL
             |
             |_(0)
        
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(3)
        avl.insert_without_balancing_height_update(0)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 3)
        self.assertEqual(avl.root.left.key, 0)
        self.assertEqual(avl.root.right.key, 10)
        self.assertIsNone(avl.root.right.left)
        self.assertIsNone(avl.root.right.right)

    def test_balance_1_3(self):
        """
        Case 1.3: The node to balance's left child has greater length and left child' s right child has greater height
        (10)---(13)
              |
              |_(3)---(5)---(7)
                     |     |
                     |     |_NIL
                     |
                     |_(0)
        Rebalance:
        (5)---(10)---(13)
             |      |
             |      |_(7)
             |
             |_(3)----NIL
                     |
                     |_(0)
        
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(13)
        avl.insert_without_balancing_height_update(3)
        avl.insert_without_balancing_height_update(0)
        avl.insert_without_balancing_height_update(5)
        avl.insert_without_balancing_height_update(7)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 5)
        self.assertEqual(avl.root.left.key, 3)
        self.assertEqual(avl.root.left.left.key, 0)
        self.assertIsNone(avl.root.left.right)
        self.assertEqual(avl.root.right.key, 10)
        self.assertEqual(avl.root.right.left.key, 7)
        self.assertEqual(avl.root.right.right.key, 13)

    def test_balance_2_1(self):
        """
        Case 2.1: The node to balance's left child has greater length and left child's childs have equal height
        (10)---(13)---(15)
              |      |
              |      |_(11) 
              |
              |_NIL
        Rebalance:
        (13)---(15)
             |
             |_(10)---(11)
                     |
                     |_NIL
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(13)
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(11)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 13)
        self.assertEqual(avl.root.right.key, 15)
        self.assertEqual(avl.root.left.key, 10)
        self.assertEqual(avl.root.left.right.key, 11)
        self.assertIsNone(avl.root.left.left)

    def test_balance_2_2(self):
        """
        Case 2.2: The node to balance's left child has greater length and left child's right child has greater height
        (10)---(13)---(15)---(20)
              |      |      |
              |      |      |_NIL
              |      |
              |      |_(11) 
              |
              |_(5)
        Rebalance:
        (13)---(15)---(20)
              |      |
              |      |_NIL
              |
              |_(10)---(11)
                      |
                      |_(5)
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(5)
        avl.insert_without_balancing_height_update(13)
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(11)
        avl.insert_without_balancing_height_update(20)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 13)
        self.assertEqual(avl.root.right.key, 15)
        self.assertEqual(avl.root.right.right.key, 20)
        self.assertIsNone(avl.root.right.left)
        self.assertEqual(avl.root.left.key, 10)
        self.assertEqual(avl.root.left.right.key, 11)
        self.assertEqual(avl.root.left.left.key, 5)

    def test_balance_2_3(self):
        """
        Case 2.3: The node to balance's left child has greater length and left child's left child has greater height
        (10)---(13)---(15)
              |      |
              |      |_(11)---(12)
              |              |
              |              |_NIL 
              |
              |_(5)
        Rebalance:
        (11)---(13)---(15)
              |      |
              |      |_(12)
              |
              |_(10)---NIL
                      |
                      |_(5)
        """  
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(10)
        avl.insert_without_balancing_height_update(5)
        avl.insert_without_balancing_height_update(13)
        avl.insert_without_balancing_height_update(15)
        avl.insert_without_balancing_height_update(11)
        avl.insert_without_balancing_height_update(12)
        avl.balance_0(avl.root)
        self.assertEqual(avl.root.key, 11)
        self.assertEqual(avl.root.right.key, 13)
        self.assertEqual(avl.root.right.right.key, 15)
        self.assertEqual(avl.root.right.left.key, 12)
        self.assertEqual(avl.root.left.key, 10)
        self.assertIsNone(avl.root.left.right)
        self.assertEqual(avl.root.left.left.key, 5)

    def test_balance_recursive(self):
        """
        To test if the whole tree is balanced when calling balance_recursive() on a leaf of the tree
        (8)---NIL
             |
             |_(5)----(6)---(7)
                     |     |
                     |     |_NIL
                     |
                     |_NIL
        Recursively balanced:
        (6)---(8)---NIL
             |     |
             |     |_(7)
             |
             |_(5)
        """
        avl=AVL_tree()
        avl.insert_without_balancing_height_update(8)
        avl.insert_without_balancing_height_update(5)
        avl.insert_without_balancing_height_update(6)
        avl.insert_without_balancing_height_update(7)
        #Manually set height to test
        avl.root.height=4
        avl.root.left.height=3
        avl.root.left.right.height=2
        avl.balance_recursive(avl.root.left.right.right)
        self.assertEqual(avl.root.key, 6)
        self.assertEqual(avl.root.left.key, 5)
        self.assertEqual(avl.root.right.key, 8)
        self.assertEqual(avl.root.right.left.key, 7)

    def test_AVL_insert_0(self):
        """
        The new node is the root of the tree
        """  
        avl=AVL_tree()
        self.assertEqual(avl.AVL_insert(10), 0)
        self.assertEqual(avl.root.key, 10)
        self.assertEqual(avl.root.height, 1)
    
    def test_AVL_insert_1(self):
        """
        To test if a new node is inserted into the AVL tree correctly
        Tree using insert_without_balancing_height_update():
        (10)---(13)---(20)---(21)
              |      |      |
              |      |      |_NIL
              |      |
              |      |_(11)
              |
              |_(5)
        Tree using AVL_insert()
        (13)---(20)---(21)
             |      |
             |      |_NIL
             |
             |_(10)---(11)
                     |
                     |_(5)
        """
        avl_0=AVL_tree()
        avl_0.insert_without_balancing_height_update(10)
        avl_0.insert_without_balancing_height_update(5)
        avl_0.insert_without_balancing_height_update(13)
        avl_0.insert_without_balancing_height_update(11)
        avl_0.insert_without_balancing_height_update(20)
        avl_0.insert_without_balancing_height_update(21)
        self.assertEqual(avl_0.root.key, 10)
        self.assertEqual(avl_0.root.left.key, 5)
        self.assertEqual(avl_0.root.right.key, 13)
        self.assertEqual(avl_0.root.right.right.key, 20)
        self.assertEqual(avl_0.root.right.right.right.key, 21)
        avl_1=AVL_tree()
        avl_1.AVL_insert(10)
        avl_1.AVL_insert(5)
        avl_1.AVL_insert(13)
        avl_1.AVL_insert(11)
        avl_1.AVL_insert(20)
        avl_1.AVL_insert(21)
        self.assertEqual(avl_1.root.key, 13)
        self.assertEqual(avl_1.root.left.key, 10)
        self.assertEqual(avl_1.root.left.right.key, 11)
        self.assertEqual(avl_1.root.left.left.key, 5)
        self.assertEqual(avl_1.root.right.key, 20)
        self.assertEqual(avl_1.root.right.right.key, 21)

if __name__ == '__main__':
    unittest.main()