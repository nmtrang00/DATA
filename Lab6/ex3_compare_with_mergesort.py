#!/bin/python
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import wilcoxon, ttest_ind
from numpy.random import randint
import numpy as np
import os
import sys
from ex2_heapsort import heapSort
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
sys.path.append(os.path.join(home_dir, "Lab2"))
from ex3_insertion_sort_merge_sort import mergeSort

"""
Both runs in O(nlog(n))
"""

def compare_sort_at_a_size(n):
    """
    Two-sided student's t-test for each size of input array.  For each size of input array, 
    H0: 2 independent samples, T_merge and T_heap have identical average expected values (T_merge-T_heap=0)
    """
    T_merge=[]
    T_heap=[]
    for i in range(4000):
        A=[]
        while len(A)<n:
            k=randint(0,n*2)
            if not k in A:
                A.append(k)
        A_merge=[k for k in A]
        A_heap=[k for k in A]
        T_merge.append(track_time(mergeSort(A_merge, 0, len(A_merge)-1)))
        T_heap.append(track_time(heapSort(A_heap)))
    d={"T_merge": T_merge, "T_heap": T_heap}
    df=pd.DataFrame(data=d).replace(0, np.NaN).dropna()
    rel=ttest_ind(df["T_merge"], df["T_heap"], alternative="two-sided")
    return p_value(rel)

def compare_sort_at_different_sizes(sizes):
    """
    Two-sided Wilcoxin
    H0: mergeSort() and heapSort() do not express significant difference in running time
    (The median difference in runtime of 2 implementations (T_merge-T_heap) is 0)
    Only works with sample greater than 60
    """
    T_merge=[]
    T_heap=[]
    testSizes=sizes[:]
    for i in range(1000):
        testSizes.extend(sizes)
    for n in testSizes:
        A=[]
        while len(A)<n:
            k=randint(0,n*2)
            if not k in A:
                A.append(k)
        print(A)
        A_merge=[k for k in A]
        A_heap=[k for k in A]
        T_merge.append(track_time(mergeSort(A_merge, 0, len(A_merge)-1)))
        T_heap.append(track_time(heapSort(A_heap)))
    d={"T_merge": T_merge, "T_heap": T_heap}
    df=pd.DataFrame(data=d).replace(0,np.nan)
    df_no_zero=df.dropna()
    rel=wilcoxon(df_no_zero["T_merge"], df_no_zero["T_heap"], alternative="two-sided")
    return p_value(rel)

        
def main():
    sizes=[15,50,100,1000]
    # for i in range(1,6):
    #     print("Attempt no.{}".format(i))
    #     for n in sizes:
    #         rel=compare_sort_at_a_size(n)
    #         print("\tn={}, Student's t-test p_value: {:.4f}".format(n, rel))
    for i in range(1,6):
        print("Attempt no.{}".format(i))
        rel=compare_sort_at_different_sizes(sizes)
        print("\tWilcoxon p-value: {:.4f}".format(rel))
    
    
main()

# def compare_sort_at_a_size_by_diagram(n):
#     """
#     To compare running_time of mergeSort() and heapSort() on a array of "n" integers 
#     Both runs in O(nlog(n))
#     """
#     T_merge=[]
#     T_heap=[]
#     for i in range(1000):
#         A=[]
#         while len(A)<n:
#             k=randint(0,n*2)
#             if not k in A:
#                 A.append(k)
#         T_merge.append(track_time(mergeSort(A, 0, len(A)-1)))
#         T_heap.append(track_time(heapSort(A)))
#     d={"mergeSort()": T_merge, 
#     "heapSort()": T_heap}
#     df=pd.DataFrame(data=d).replace(0, np.NaN).dropna()
#     ax = sns.boxplot(data=df, palette="Blues")
#     ax.set_title("n={}".format(n))
#     ax.set_ylabel("Running time (s)")
#     plt.show()