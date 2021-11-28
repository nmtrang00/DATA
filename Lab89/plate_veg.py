#!/bin/python
import unittest
import os
import sys
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
sys.path.append(os.path.join(home_dir, "Lab4"))
from Lab4.doubly_linked_list import doubly_linked_list, node

class node_plate(node):
    def __init__(self, key):
        node.__init__(self, key)
        self.linked=None 

class Stack():
    def __init__(self):
        self.content=doubly_linked_list()

    def stackEmpty(self):
        """
        To check if the stack is empty, ie. Stack.content.head is not linked to another node
        but np.nan as the characteristic inherited from the singly linked list
        O(1)
        """
        if self.content.head.next == None:
            return True
        else:
            return False

    def push(self, newPlate):
        """
        To add an element to the stack
        O(1): list.insert() runs in O(1)
        """
        new_node_plate=node_plate(newPlate)
        self.content.insert(new_node_plate)
        return new_node_plate

    def pop(self):
        """
        To remove the most recently added node, ie. node_0
        O(1): list.delete() runs in O(1)
        """
        if self.stackEmpty():
            raise Exception("Underflow")
        else:
            node_plate_to_pop=self.content.head.next
            self.content.delete(self.content.head.next)
            return node_plate_to_pop

    def peek(self):
        """
        To get value of the most recently added node in the stack
        O(1)
        """
        if self.stackEmpty():
            raise Exception("Underflow")
        else:
            return self.content.head.next

class Plate():
    def __init__(self, vegetable):
        self.vegetable=vegetable
        self.linked_plates=Stack()
        
    def add_linked_plate(self, linked_plate_pos):
        return self.linked_plates.push(linked_plate_pos)

    def different_vegetable(self, linked_plate):
        """
        To check if the vegetable on the linked plate is different from the current plate
        O(1)
        """
        if self.vegetable != linked_plate.vegetable:
            return True
        else:
            return False
    
    def del_linked_node_plate(self, linked_node_plate):
        """
        To check if the vegetable on the linked plate is different from the current plate
        O(1): doubly_linked_list.delete() runs in O(1)
        """
        self.linked_plates.content.delete(linked_node_plate)

    def pop_linked_node_plate(self):
        """
        To remove the last plate added to the "linked_plates" stack and linked to the current plate
        """
        return self.linked_plates.pop()

    def linked_plates_empty(self):
        return self.linked_plates.stackEmpty()

class Veg_on_plate():
    """
    2 conditions to meet:
        (1) Each plate has only one type of vegetable => To be checked in check_condition_1()
        (2) No 2 plates joined by straw have the same type of vegetable => To be checked in check_condition_2_greedy() or check_condition_2()
    Output:
        TRUE: Both conditions are met
        FALSE: Either of condition (1) or (2) is not met
    """
    def __init__(self, n_plate, n_type_vegetable, n_straw, veg_order, plate_links):
        """
        All numbers are integer
        n_plate: Number of plate used
        n_type_vegetable: Number of types of vegetable used 
        n_straw: Number of straw used to connect plates 
        veg_order: A 1D array show how vegetable are set on each plate in order from plate 0 to plate (n_plate-1) 
        plate_links: A 2D array, each row contains a couple of plates linked with each other
        plates: A 1D array to store all plates
        """
        self.n_plate=n_plate
        self.n_type_vegetable=n_type_vegetable
        self.n_straw=n_straw
        self.veg_order=veg_order
        self.plate_links=plate_links
        self.plates=[None]*n_plate

    def check_n_plate(self):
        """
        n_plate > 0
        """
        if self.n_plate < 0:
            raise Exception("Error 0: The number of plate must be a positive integer ")
    
    def check_n_type_vegetable(self):
        """
        0 < n_type_vegetable <= n_plate
        n_type_vegetable > n_plate means that there are at least a plate with more than 1 vegetable, violating (1)
        """
        if self.n_type_vegetable > 0:
            if self.n_type_vegetable > self.n_plate:
                return False
        else:
            raise Exception("Error 1: The number of vegetable must be a positive integer ")
    
    def check_n_straw(self):
        """
        0 <= n_staw <= n_plate*(n_plate-1)/2, each plate can be linked with maximum other (n_plate - 1) plates
        """
        if self.n_straw < 0 or  self.n_straw > self.n_plate*(self.n_plate-1)/2:
            raise Exception("Error 2: The number of straw must be a positive integer in range 0 and n_plate*(n_plate-1)/2, inclusively. Each plate can be linked to maximum other {} plates.".format(n_plate-1))
    
    def check_veg_order(self):
        """
        len(veg_order) == n_plate, (1) is violated if there is any plate is empty
        0 <= veg_order[i] < n_type_vegetable for i in range(len(veg_order))
        """
        if len(self.veg_order) == self.n_plate:
            for i in range(self.n_plate):
                veg=self.veg_order[i]
                if veg >= 0 and veg < self.n_type_vegetable:
                    self.plates[i]=Plate(self.veg_order[i])
                else:
                    raise Exception("Error 3: The vegetable must be an integer in range of 0 and n_vegtable-1, inclusively")
        elif len(self.veg_order) > self.n_plate:
            raise Exception("Error 4: There are only {} plates, but the order of vegetable on {} plates is given.".format(self.n_plate, len(self.veg_order)))
        elif len(self.veg_order) < self.n_plate:
            return False
    
    def check_plate_links(self):
        """
        len(plate_links) == n_straw, 0 <= plate_links[i][j] < n_plate for i,j in range(n_plate)
        """
        if  len(self.plate_links) == self.n_straw:
            for i in range(self.n_straw):
                couple=self.plate_links[i]
                plate_A=couple[0]
                plate_B=couple[1]
                if (plate_A >= 0 and plate_A < self.n_plate) and (plate_B >= 0 and plate_B < self.n_plate):
                    node_plate_B=self.plates[plate_A].add_linked_plate(plate_B)
                    node_plate_A=self.plates[plate_B].add_linked_plate(plate_A)
                    node_plate_A.linked=node_plate_B
                    node_plate_B.linked=node_plate_A
                else:
                    raise Exception("Error 5: Linked plates must be in range of plate 0 to plate (n_plate-1), inclusively")
        else:
            raise Exception("Error 6: There are {} staws, but {} couples of linkesd plates are given".format(self.n_straw, len(self.plate_links)))
    
    def check_condition_1(self):
        """
        To check conditions of all attributes
        """
        self.check_n_plate()
        self.check_n_type_vegetable()
        self.check_n_straw()
        self.check_veg_order()
        self.check_plate_links()
        
    def check_condition_2_greedy(self):
        if self.n_plate == self.n_type_vegetable:
            """
            Each plate contains a unique type of vegetable => It doesn't matter how they are connected
            """
            return True

    def check_condition_2(self):
        if self.n_plate == self.n_type_vegetable:
            """
            Each plate contains a unique type of vegetable => It doesn't matter how they are connected
            """
            return True
        for i in range(self.n_plate):
            plate_to_check=self.plates[i]
            # print(plate_to_check, self.plates[i])
            while not plate_to_check.linked_plates_empty():
                popped_node_plate=plate_to_check.pop_linked_node_plate()
                popped_plate=self.plates[popped_node_plate.key]
                if popped_plate.vegetable == plate_to_check.vegetable:
                    return False
                else:
                    popped_plate.del_linked_node_plate(popped_node_plate.linked)
        return True           

    def run_check(self):
        return self.check_condition_1() and self.check_condition_2()
    

class TestFunctions(unittest.TestCase):
    #node_plate
    def test_node_plate_init(self):
        np=node_plate(0)
        self.assertEqual(np.key, 0)
        self.assertEqual(np.prev, None)
        self.assertEqual(np.next, None)
        self.assertEqual(np.linked, None)

    #Stack
    def test_stack_init(self):
        S=Stack()
        self.assertIsInstance(S.content, doubly_linked_list)
        self.assertIsNone(S.content.head.key)

    def test_stack_push(self):
        S=Stack()
        new_node_plate=S.push(5)
        self.assertIsInstance(new_node_plate, node_plate)
        self.assertEqual(S.content.head.next.key, 5)
        self.assertEqual(S.content.head.next.next, None)
        self.assertEqual(S.content.head.next.prev, S.content.head)

    def test_stack_empty(self):
        S=Stack()
        self.assertTrue(S.stackEmpty())
        S.push(node(5))
        self.assertFalse(S.stackEmpty())
        
    def test_stack_pop(self):
        S=Stack()
        S.push(4)
        S.push(5)
        popped_node=S.pop()
        self.assertIsInstance(popped_node, node_plate)
        self.assertEqual(popped_node.key, 5)
        self.assertEqual(S.content.head.next.key, 4)
    
    def test_stack_peek(self):
        S=Stack()
        S.push(4)
        S.push(5)
        peeked_node=S.peek()
        self.assertEqual(peeked_node.key, 5)
        self.assertEqual(S.content.head.next.key, 5)

    #Plate
    def test_plate_init(self):
        p=Plate(0)
        self.assertEqual(p.vegetable, 0)
        self.assertIsInstance(p.linked_plates, Stack)
    
    def test_plate_add_linked_plate(self):
        p0=Plate(0)
        p1=Plate(1)
        P=[p0, p1]
        np1=P[0].add_linked_plate(1)
        self.assertFalse(p0.linked_plates.stackEmpty())
        self.assertEqual(p0.linked_plates.content.head.next.key, 1)
        self.assertEqual(np1.key, 1)
    
    def test_plate_diff_veg(self):
        p0=Plate(0)
        p1=Plate(1)
        p2=Plate(0)
        self.assertTrue(p0.different_vegetable(p1))
        self.assertFalse(p0.different_vegetable(p2))

    def test_plate_del_linked_plate(self):
        p0=Plate(0)
        p1=Plate(1)
        np1=p0.add_linked_plate(p1)
        p0.del_linked_node_plate(np1)
        self.assertTrue(p0.linked_plates.stackEmpty())

    def test_plate_pop_linked_plate(self):
        p0=Plate(0)
        p1=Plate(1)
        np1=p0.add_linked_plate(p1)
        np0=p1.add_linked_plate(p0)
        popped_node_plate=p0.pop_linked_node_plate()
        self.assertEqual(popped_node_plate.key, p1)
        self.assertIsNone(p0.linked_plates.content.head.next)
        self.assertFalse(p1.linked_plates_empty())
        
    def test_plate_linked_plates_empty(self):
        p0=Plate(0)
        self.assertTrue(p0.linked_plates_empty())
        p0.add_linked_plate(Plate(1))
        self.assertFalse(p0.linked_plates_empty())

    #Veg_on_plate
    def test_vp_init(self):
        n_plate=-1
        n_type_vegetable=4
        n_straw=4
        veg_order=[0, 1, 2, 3]
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        self.assertEqual(vp.n_plate, -1)
        self.assertEqual(vp.n_type_vegetable, 4)
        self.assertEqual(vp.n_straw, 4)
        self.assertEqual(vp.veg_order, [0, 1, 2, 3])
        self.assertEqual(vp.plate_links[3], [2,3])

    def test_vp_n_plate(self):
        """
        To test n_plate condition
        """
        n_plate=-1
        n_type_vegetable=4
        n_straw=4
        veg_order=[0, 1, 2, 3]
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        with self.assertRaises(Exception): vp.check_n_plate() #Error 0

    def test_vp_n_veg(self):
        """
        To test n_type_vegetable condition
        """
        n_plate=4
        n_type_vegetable=-10
        n_straw=4
        veg_order=[0, 1, 2, 3]
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        with self.assertRaises(Exception): vp.check_n_type_vegetable() #Error 1
        n_type_vegetable_1=5
        vp1=Veg_on_plate(n_plate, n_type_vegetable_1, n_straw, veg_order, plate_links)
        self.assertFalse(vp1.check_n_type_vegetable())

    def test_vp_n_straw(self):
        """
        To test n_straw condition
        """
        n_plate=4
        n_type_vegetable=4
        n_straw=-1
        veg_order=[0, 1, 2, 3]
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        with self.assertRaises(Exception): vp.check_n_straw() #Error 2
        n_straw_1=7 #n_plate*(n_plate-1)/2=4*3/2=6)
        vp1=Veg_on_plate(n_plate, n_type_vegetable, n_straw_1, veg_order, plate_links)
        with self.assertRaises(Exception): vp1.check_n_straw() #Error 2

    def test_vp_veg_order(self):
        """
        To test veg_order condition
        """
        n_plate=4
        n_type_vegetable=4
        n_straw=4
        veg_order=[0, 1, 2, 3] 
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        vp.check_veg_order()
        self.assertIsInstance(vp.plates[0], Plate)
        self.assertEqual(vp.plates[2].vegetable, 2)
        veg_order1=[0, 1, 2, 4]
        vp1=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order1, plate_links)
        with self.assertRaises(Exception): vp1.check_veg_order() #Error 3
        veg_order2=[0, 1, 2, 2, 1]
        vp2=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order2, plate_links)
        with self.assertRaises(Exception): vp2.check_veg_order() #Error 4
        veg_order3=[0, 1, 2]
        vp3=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order3, plate_links)
        self.assertFalse(vp3.check_veg_order())

    def test_vp_plate_links(self):
        """
        To test veg_order condition
        (check_veg_order() passed the test)
        """
        n_plate=4
        n_type_vegetable=4
        n_straw=1
        veg_order=[0, 1, 2, 3] 
        plate_links=[[0, 1]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        vp.check_veg_order()
        vp.check_plate_links()
        self.assertFalse(vp.plates[0].linked_plates.stackEmpty())
        self.assertEqual(vp.plates[0].linked_plates.content.head.next.key, 1)
        self.assertEqual(vp.plates[0].linked_plates.content.head.next.linked, 
        vp.plates[1].linked_plates.content.head.next)
        plate_links_1=[[0, 1],
                     [0, 3],
                     [1, 2]]
        vp1=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links_1)
        with self.assertRaises(Exception): 
            vp1.check_veg_order()
            vp1.check_plate_links() #Error 6
        plate_links_2=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3],
                     [0, 2]]
        vp2=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links_2)
        with self.assertRaises(Exception): 
            vp2.check_veg_order()
            vp2.check_plate_links() #Error 6
        plate_links_3=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 4]] 
        vp3=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links_3)
        with self.assertRaises(Exception): 
            vp3.check_veg_order()
            vp3.check_plate_links() #Error 5

    # def test_vp_condition_2_greedy_0(self):
    #     """
    #     True is returned when the number of plate is equal to the number of types of vegetable distributed on plate
    #     """
    #     n_plate=4
    #     n_type_vegetable=4
    #     n_straw=4
    #     veg_order=[0, 1, 2, 3] 
    #     plate_links=[[0, 1],
    #                  [0, 3],
    #                  [1, 2],
    #                  [2, 3]]
    #     vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
    #     vp.check_condition_2_greedy()

    def test_vp_condition_2_0(self):
        """
        True is returned when the number of plate is equal to the number of types of vegetable distributed on plate
        """
        n_plate=4
        n_type_vegetable=4
        n_straw=4
        veg_order=[0, 1, 2, 3] 
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        vp.check_condition_1()
        self.assertTrue(vp.check_condition_2())

    def test_vp_condition_2_1(self):
        """
        False is returned when 2 linked plates have the same type of vegetable
        """
        n_plate=4
        n_type_vegetable=3
        n_straw=4
        veg_order=[0, 1, 0, 2] 
        plate_links=[[0, 1],
                     [0, 2],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        vp.check_condition_1()
        self.assertFalse(vp.check_condition_2()) #Plates 0 and 2 are linked, but they both have vegetable of type 0
    
    def test_vp_condition_2_2(self):
        """
        True is returned when condition 2 is matched 
        """
        n_plate=4
        n_type_vegetable=3
        n_straw=4
        veg_order=[0, 1, 0, 2] 
        plate_links=[[0, 1],
                     [0, 3],
                     [1, 2],
                     [2, 3]]
        vp=Veg_on_plate(n_plate, n_type_vegetable, n_straw, veg_order, plate_links)
        vp.check_condition_1()
        self.assertTrue(vp.check_condition_2())

if __name__ == '__main__':
    unittest.main()

