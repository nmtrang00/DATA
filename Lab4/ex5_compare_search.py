#!/bin/python

import math
import time
import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon

import os
import sys
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
sys.path.append(os.path.join(home_dir,'Lab3'))
from ex3_singly_linked_list import singly_linked_list
from ex4_binary_search_tree import node, binary_search_tree
from doubly_linked_list import doubly_linked_list
from ex5_find_key_in_BST import iterative_tree_search

def array_search(array, key):
    for i in range(len(array)):
        if array[i]==key:
            return i
    return -1

def bst_search_running_time_against_size(maxSize):
    """
    To compare running time of iterative_treee_search() agains the size of the tree
    For each iternation, a new element is added to the tree, which means the tree size increases by one.
    """
    T_bst=dict()
    bst=binary_search_tree()
    key_to_find=-1
    keys=[]
    for n in range(maxSize):
        print(n)
        k=randint(0,maxSize*2)
        while k in keys:
            k=randint(0,maxSize*2)
        keys.append(k)
        bst.insert(k)
        t=track_time(iterative_tree_search(bst, key_to_find))
        if t!=0:
            T_bst[n]=t
    # print(T_bst)
    ax=sns.regplot(x=[k for k in T_bst.keys()], y=[v for v in T_bst.values()], logx=True)
    # plt.plot([k for k in T_bst.keys()], [v for v in T_bst.values()])
    plt.show()

def compare_search_at_different_sizes(maxSize):
    """
    One-sided Wilcoxin
    H0: Searching for an element in a binary search tree takes less time than in array/singly linked list/doubly linked list
    (The median difference in runtime of 2 implementations (T_bst-T_another_function) is negative)
    For each iternation, a new element is added to the tree, which means the tree size increases by one.
    """
    T_bst=[]
    T_arr=[]
    T_singly_linked_list=[]
    T_doubly_linked_list=[]
    key_to_find=-1
    keys=[]
    bst=binary_search_tree()
    sll=singly_linked_list()
    dll=doubly_linked_list()
    for n in range(maxSize):
        # print(n)
        k=randint(0,maxSize*2)
        while k in keys:
            k=randint(0,maxSize*2)
        keys.append(k)
        arr=np.array(keys)
        sll.insert(k)
        dll.insert(node(k))
        bst.insert(k)
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find), "time"))
        T_arr.append(track_time(array_search(arr, key_to_find), "time"))
        T_singly_linked_list.append(track_time(sll.search(key_to_find), "time"))
        T_doubly_linked_list.append(track_time(dll.search(key_to_find), "time"))
    d={"T_bst": T_bst, "T_arr": T_arr, "T_sll": T_singly_linked_list, "T_dll": T_doubly_linked_list}
    rel_bst_arr=wilcoxon(d["T_bst"], d["T_arr"], alternative="greater")
    rel_bst_sll=wilcoxon(d["T_bst"], d["T_sll"], alternative="greater")
    rel_bst_dll=wilcoxon(d["T_bst"], d["T_dll"], alternative="greater")
    return p_value(rel_bst_arr), p_value(rel_bst_sll), p_value(rel_bst_dll)

def compare_search_at_a_size(n):
    T_bst=[]
    T_arr=[]
    T_singly_linked_list=[]
    T_doubly_linked_list=[]
    key_to_find=math.inf
    for i in range(1000):
        print(i)
        keys=[]
        while len(keys)<n:
            k=randint(0,n*2)
            if not k in keys:
                keys.append(k)
        # print(keys)
        bst=binary_search_tree()
        sll=singly_linked_list()
        dll=doubly_linked_list()
        arr=np.array(keys)
        for k in keys:
            bst.insert(k)
            sll.insert(k)
            dll.insert(node(k))
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find)))
        T_arr.append(track_time(array_search(arr, key_to_find)))
        T_singly_linked_list.append(track_time(sll.search(key_to_find)))
        T_doubly_linked_list.append(track_time(dll.search(key_to_find)))
        # print(iterative_tree_search(bst, key_to_find))
        # print(array_search(arr, key_to_find))
        # print(sll.search(key_to_find))
        # print(dll.search(key_to_find))
    d={"bst": T_bst, 
    "array": T_arr, 
    "singly linked list": T_singly_linked_list, 
    "doubly linked list": T_doubly_linked_list}
    df=pd.DataFrame(data=d).replace(0, np.NaN).dropna()
    ax = sns.boxplot(data=df, palette="Blues")
    plt.show()

def main():
    # bst_search_running_time_against_size(10000)
    # compare_search_at_a_size(200)
    # box_plot_tree_balanced()
    for i in range(1,5):
        print("Attempt no.{}".format(i))
        results=compare_search_at_different_sizes(2000)
        print("\tp_value_bst_arr: {:.4f}".format(results[0]))
        print("\tp_value_bst_sll: {:.4f}".format(results[1]))
        print("\tp_value_bst_dll: {:.4f}".format(results[2]))

main()

