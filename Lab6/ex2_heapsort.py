#!/bin/python

import unittest
from ex1_maxHeap import maxHeap

def heapSort(A):
    """
    To sort an array A using maxHeap:
    1. Create a maxHeap from A, O(nlog(n)) (tighter bound as O(n))
    2. Extract max of the heap (ie. delete maxHeap[0]) till there is nothing left in the heap, O(n(log(n)))

    O(nlog(n))
    """
    rel=[]
    H=maxHeap()
    H.build_max_heap(A)
    while H.tail>0:
        rel.append(H.content[0])
        H.delete(0)
    return rel

class TestStackQueueMethods(unittest.TestCase):
    def test_heapSort(self):
            """
            To test if after a node of the heap is deleted, the heap property is maintained
            (16)---(15)---(13)
                |      |
                |      |_(14)---NIL
                |              |
                |              |_(10)
                |
                |_(9)---(7)---(3)
                        |     |
                        |     |_(1)
                        |
                        |_(8)---(5)
                                |
                                |_(4)
            """
            rel=heapSort([16, 9, 15, 8, 7, 14, 13, 4, 5, 1, 3, 10])
            expected_arr=[16, 15, 14, 13, 10, 9, 8, 7, 5, 4, 3, 1]
            self.assertEqual(rel, expected_arr)

if __name__ == '__main__':
    unittest.main()