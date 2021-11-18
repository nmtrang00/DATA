#!/bin/python
import math
import numpy as np
import seaborn as sns
from numpy.random import randint
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
import pandas as pd
import os
import sys
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
sys.path.append(os.path.join(home_dir,'Lab4'))
from ex4_binary_search_tree import binary_search_tree
from ex5_find_key_in_BST import iterative_tree_search
from ex2_AVL_tree import AVL_tree

def compare_insert_at_a_size(n):
    """
    To compare running_time() of bst.insert() and avl.AVL_insert() when inserting n elements into the tree
    Both runs in O(log(n))
    """
    T_bst=[]
    T_avl=[]
    for i in range(200):
        print(i)
        keys=[]
        while len(keys)<n:
            k=randint(0,n*2)
            if not k in keys:
                keys.append(k)
        bst=binary_search_tree()
        avl=AVL_tree()
        bst_time=0
        avl_time=0
        for k in keys:
            bst_time+=track_time(bst.insert(k))
            avl_time+=track_time(avl.AVL_insert(k))
        T_bst.append(bst_time)
        T_avl.append(avl_time)
    d={"bst_insert": T_bst,"avl_insert": T_avl}
    ax = sns.boxplot(data=pd.DataFrame(data=d))
    ax.set(xlabel='Functions', ylabel='Running_time (s)')
    plt.show()

def compare_insert_at_different_sizes(maxSize):
    """
    Two-sided Wilcoxin
    H0: bst.insert() and avl.AVL_insert() do not express significant difference in running time
    For each iternation, a new element is added to the tree, which means the tree size increases by one.
    """
    T_bst=[]
    T_avl=[]
    bst=binary_search_tree()
    avl=AVL_tree()
    keys=[]
    for n in range(maxSize):
        newKey=randint(0,maxSize*2)
        while newKey in keys:
            newKey=randint(0,maxSize*2)
        keys.append(newKey)
        T_bst.append(track_time(bst.insert(newKey)))
        T_avl.append(track_time(avl.AVL_insert(newKey)))
    rel_stats=wilcoxon(T_bst,T_avl,alternative="two-sided")
    return p_value(rel_stats)

def compare_search_at_a_size(n):
    """
    To compare running time of iterative_tree_search() on bst and avl of size 
    Both runs in O(log(n))
    """
    T_bst=[]
    T_avl=[]
    key_to_find=-1
    for i in range(200):
        print(i)
        keys=[]
        while len(keys)<n:
            k=randint(0,n*2)
            if not k in keys:
                keys.append(k)
        bst=binary_search_tree()
        avl=AVL_tree()
        for k in keys:
            bst.insert(k)
            avl.AVL_insert(k)
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find)))
        T_avl.append(track_time(iterative_tree_search(avl, key_to_find)))
    # print(T_bst, T_avl)
    d={"bst_search": T_bst,"avl_search": T_avl}
    ax = sns.boxplot(data=pd.DataFrame(data=d).replace(0, np.NaN))
    ax.set(xlabel='Functions', ylabel='Running_time (s)')
    plt.show()

def compare_search_at_different_sizes(maxSize):
    """
    Two-sided Wilcoxin
    H0: iterative_tree_search() on bst and avl do not express significant difference in running time
    For each iternation, a new element is added to the tree, which means the tree size increases by one.
    """
    T_bst=[]
    T_avl=[]
    bst=binary_search_tree()
    avl=AVL_tree()
    key_to_find=-1
    keys=[]
    for n in range(maxSize):
        newKey=randint(0,maxSize*2)
        while newKey in keys:
            newKey=randint(0,maxSize*2)
        keys.append(newKey)
        bst.insert(newKey)
        avl.AVL_insert(newKey)
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find)))
        T_avl.append(track_time(iterative_tree_search(avl, key_to_find)))
    rel_stats=wilcoxon(T_bst,T_avl,alternative="two-sided")
    return p_value(rel_stats)

def compare_search_worst_case_at_a_size(n):
    """
    To compare the running time of the iterative search in the worst case 
    where the key inserted in the tree in increasing or decreasing order
    """
    T_bst=[]
    T_avl=[]
    key_to_find=math.inf
    for i in range(200):
        print(i)
        s=randint(0,n*2)
        diff=randint(1,n)
        keys=range(s,(n-1)*diff+s,diff)
        print(keys)      
        bst=binary_search_tree()
        avl=AVL_tree()
        for k in keys:
            bst.insert(k)
            avl.AVL_insert(k)
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find)))
        T_avl.append(track_time(iterative_tree_search(avl, key_to_find)))
    # print(T_bst, T_avl)
    d={"bst_search": T_bst,"avl_search": T_avl}
    ax = sns.boxplot(data=pd.DataFrame(data=d).replace(0, np.NaN))
    ax.set(xlabel='Functions', ylabel='Running_time (s)')
    plt.show()

def compare_worst_case_search_at_different_sizes(maxSize):
    """
    One-sided Wilcoxin
    H0: iterative_tree_search() on bst is less efficient in running time than avl.
    (T_bst-T_avl<0)
    For each iternation, a new element is added to the tree, which means the tree size increases by one.
    """
    T_bst=[]
    T_avl=[]
    bst=binary_search_tree()
    avl=AVL_tree()
    key_to_find=-1
    key=0
    diff=randint(1,maxSize)
    for n in range(maxSize):
        bst.insert(key)
        avl.AVL_insert(key)
        key+=diff
        T_bst.append(track_time(iterative_tree_search(bst, key_to_find)))
        T_avl.append(track_time(iterative_tree_search(avl, key_to_find)))
    rel_stats=wilcoxon(T_bst,T_avl,alternative="less")
    return p_value(rel_stats)

def main():
    compare_insert_at_a_size(20)
    for i in range(1,5):
        print("Attempt no.{}:".format(i))
        print("\tpvalue_insert:", round(compare_insert_at_different_sizes(100),5))
    # compare_search_at_a_size(20)
    # for i in range(1,5):
    #     print("Attempt no.{}:".format(i))
    #     print("\tpvalue_search:", round(compare_search_at_different_sizes(100),5))
    # compare_search_worst_case_at_a_size(20)
    # for i in range(1,5):
    #     print("Attempt no.{}:".format(i))
    #     print("\tpvalue_search:", round(compare_worst_case_search_at_different_sizes(1000),5))
main()