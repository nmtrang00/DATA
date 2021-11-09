#!/bin/python

import unittest
import sys

sys.path.append('/Users/trangnguyen/Documents/Study/DATA/Lab4')
from ex3_binary_tree import node, binary_tree
from ex4_binary_search_tree import binary_search_tree

class bst_rotate(binary_search_tree):
    def __init__(self):
        binary_search_tree.__init__(self)

    def rotate_left(self, node_to_rotate):
        """
        To exchange the position of a node with its right child 
        -X---Y---theta    ====>   -Y---theta
            |   |                     |    
            |   |_beta                |_X---beta    
            |                              | 
            |_aplha                        |_alpha
        O(1)
        """
        if node_to_rotate.right == None:
            return -1
        right_child=node_to_rotate.right
        node_to_rotate.right=right_child.left
        right_child.parent=node_to_rotate.parent
        if node_to_rotate.parent==None:
            self.root=right_child
        elif node_to_rotate.parent.left==node_to_rotate:
            node_to_rotate.parent.left=right_child
        else:
            node_to_rotate.parent.right=right_child
        right_child.left=node_to_rotate
        node_to_rotate.parent=right_child

    def rotate_right(self, node_to_rotate):
        """
        To exchange the position of a node with its left child
        -X---alpha         ====>    -Y---X---alpha
            |                           |   |
            |_Y---theta                 |   |_theta
                 |                      |
                 |_beta                 |_beta
        O(1)
        """
        if node_to_rotate.left==None:
            return -1
        left_child=node_to_rotate.left
        node_to_rotate.left=left_child.right
        left_child.parent=node_to_rotate.parent
        if node_to_rotate.parent==None:
            self.root=left_child
        elif node_to_rotate.parent.left==node_to_rotate:
            node_to_rotate.parent.left=left_child
        else:
            node_to_rotate.parent.right=left_child
        left_child.right=node_to_rotate
        node_to_rotate.parent=left_child
    
class TestbstRotateMethods(unittest.TestCase):
    def test_bst_rotate_init(self):
        """
        To test if a bst is initialised successfully
        """
        bst=bst_rotate()
        self.assertIsInstance(bst, binary_search_tree)
    
    def test_rotate_left_0(self):
        """
        To test if -1 is returned when the node to rotate does not have right child
        (15)---NIL  
              |
              |_(6)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(6)
        self.assertEqual(bst.rotate_left(bst.root), -1)

    def test_rotate_left_1(self):
        """
        To test if a node is left rotated correctly when it is the left child of another node
        (15)---(18)---(20)
              |      |
              |      |_(17)
              |
              |_(6)
        Left-rotated:
        (18)---(20) 
              |
              |_(15)---(17)
                      |
                      |_(6)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(6)
        bst.insert(18)
        bst.insert(17)
        bst.insert(20)
        bst.rotate_left(bst.root)
        self.assertAlmostEqual(bst.root.key, 18)
        self.assertAlmostEqual(bst.root.right.key, 20)
        self.assertAlmostEqual(bst.root.left.key, 15)
        self.assertAlmostEqual(bst.root.left.right.key, 17)
        self.assertAlmostEqual(bst.root.left.left.key, 6)
        
    def test_rotate_left_2(self):
        """
        To test if a node is left rotated correctly when it is the left child of another node
        (15)---(18) 
              |
              |_(6)---(7)---(13)  
                     |     |
                     |     |_NIL
                     |
                     |_(3)
        Left-rotated:
        (15)---(18) 
              |
              |_(7)---(13)  
                     |
                     |_(6)----NIL
                             |
                             |_(3)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(6)
        bst.insert(7)
        bst.insert(3)
        bst.insert(13)
        bst.insert(18)
        bst.rotate_left(bst.root.left)
        self.assertEqual(bst.root.left.key, 7)
        self.assertEqual(bst.root.left.right.key, 13)
        self.assertEqual(bst.root.left.left.key, 6)
        self.assertIsNone(bst.root.left.left.right)
        self.assertEqual(bst.root.left.left.left.key, 3)

    def test_rotate_left_3(self):
        """
        To test if a node is left rotated correctly when it is the right child of another node
        (15)---(18)---(20)---NIL
              |      |      |
              |      |      |_(19)
              |      |
              |      |_(17)
              |
              |_(6)
        Left rotated:
        (15)---(20)---NIL    
              |      |
              |      |_(18)---(19)
              |              |
              |              |_(17)
              |
              |_(6)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(6)
        bst.insert(18)
        bst.insert(20)
        bst.insert(17)
        bst.insert(19)
        bst.rotate_left(bst.root.right)
        self.assertEqual(bst.root.right.key, 20)
        self.assertIsNone(bst.root.right.right)
        self.assertEqual(bst.root.right.left.key, 18)
        self.assertEqual(bst.root.right.left.right.key, 19)
        self.assertEqual(bst.root.right.left.left.key, 17)

    def test_rotate_right_0(self):
        """
        To check if -1 is returned when the node to rotate has no left child
        (15)---(18)
              |
              |_NIL
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(18)
        self.assertEqual(bst.rotate_right(bst.root),-1)

    def test_rotate_right_1(self):
        """
        To test if a node is right-rotated correctly when it is the root of the tree
        (15)---(18)
              |
              |_(6)---(7)
                     |
                     |_(3)
        Right-rotated:
        (6)---(15)---(18)
             |      |
             |      |_(7)
             |
             |_(3)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(18)
        bst.insert(6)
        bst.insert(7)
        bst.insert(3)
        bst.rotate_right(bst.root)
        self.assertEqual(bst.root.key, 6)
        self.assertEqual(bst.root.left.key, 3)
        self.assertEqual(bst.root.right.key, 15)
        self.assertEqual(bst.root.right.right.key, 18)
        self.assertEqual(bst.root.right.left.key, 7)
    
    def test_rotate_right_2(self):
        """
        To test if a node is right-rotated correctly when it is the left child of another node
        (15)---(18)
              |
              |_(6)---(7)
                     |
                     |_(3)---(5)
                            |
                            |_(1)
        Right-rotated:
        (15)---(18)
              |
              |_(3)---(6)---(7)
                     |     |
                     |     |_(5)
                     |
                     |_(1)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(18)
        bst.insert(6)
        bst.insert(7)
        bst.insert(3)
        bst.insert(5)
        bst.insert(1)
        bst.rotate_right(bst.root.left)
        self.assertEqual(bst.root.left.key, 3)
        self.assertEqual(bst.root.left.left.key, 1)
        self.assertEqual(bst.root.left.right.key, 6)
        self.assertEqual(bst.root.left.right.right.key, 7)
        self.assertEqual(bst.root.left.right.left.key, 5)

    def test_rotate_right_3(self):
        """
        To test if a node is right-rotated correctly when it is the right child of another node
        (15)---(18)---(20)
              |      |
              |      |_(16)---(17)
              |              |
              |              |_(15)
              |_(6)
        Right-rotated:
        (15)---(16)---(18)---(20)
              |      |      |
              |      |      |_(17)
              |      |_(15)
              |
              |_(6)
        """
        bst=bst_rotate()
        bst.insert(15)
        bst.insert(18)
        bst.insert(20)
        bst.insert(16)
        bst.insert(17)
        bst.insert(15)
        bst.rotate_right(bst.root.right)
        self.assertEqual(bst.root.right.key, 16)
        self.assertEqual(bst.root.right.left.key, 15)
        self.assertEqual(bst.root.right.right.key, 18)
        self.assertEqual(bst.root.right.right.right.key, 20)
        self.assertEqual(bst.root.right.right.left.key, 17)

if __name__ == '__main__':
    unittest.main()