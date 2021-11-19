#!/bin/python

import os
import sys
import pandas as pd
import numpy as np
from numpy.random import randint
from scipy.stats import wilcoxon
import itertools
from ex1_quick_sort import quickSort
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
sys.path.append(os.path.join(home_dir, "Lab2"))
from ex3_insertion_sort_merge_sort import mergeSort, insertionSort
sys.path.append(os.path.join(home_dir, "Lab6"))
from ex2_heapsort import heapSort
import matplotlib.pyplot as plt 

"""
Time complexity:
quickSort(): O(n^2) worst case, O(nlog(n)) avg case
mergeSort(): O(nlog(n))
heapSort(): O(nlog(n))
insertionSort(): O(n^2)
Expectation: T_insertion > T_quick ~ T_merge ~ T_heap
"""

def generate_arr_to_test(n, outdir):
    """
    To create testing array
    """
    df=pd.DataFrame()
    arr=[]
    for i in range(1000):
        A=[]
        while len(A)<n:
            k=randint(0,n*2)
            if not k in A:
                A.append(k)
        arr.append(A)
    df["A"]=arr
    df.to_csv(outdir, index=False, sep="\t")
    
def collect_data(arr_to_test, time_type, outdir=None):
    """
    To track runningtime of 4 sorting functions
    """
    arr=pd.read_csv(arr_to_test, sep="\t", header=0)
    d={ "T_insertion":[], "T_quick": [], "T_merge": [], "T_heap": []}
    # for i in range(arr.shape[0]):
    for i in range(100):
        A=arr["A"][i][1:len(arr["A"][i])-1].split(",")
        t_i=0
        count_i=0
        while t_i==0 and count_i<100:
            A_insertion=[int(i) for i in A]
            t_i=track_time(insertionSort(A_insertion),time_type)
            count_i+=1
        d["T_insertion"].append(t_i)
        t_q=0
        count_q=0
        while t_q==0 and count_q<100:
            A_quick=[int(i) for i in A]
            t_q=track_time(quickSort(A_quick, 0, len(A_quick)), time_type)
            count_q+=1
        d["T_quick"].append(t_q)
        t_m=0
        count_m=0
        while t_m==0 and count_m<100:
            A_merge=[int(i) for i in A]
            t_m=track_time(mergeSort(A_merge,0, len(A_merge)-1), time_type)
            count_m+=1
        d["T_merge"].append(t_m)
        t_h=0
        count_h=0
        while t_h==0 and count_h<100:
            A_heap=[int(i) for i in A]
            t_h=track_time(heapSort(A_heap))
            count_h+=1
        d["T_heap"].append(t_h)
    df=pd.DataFrame(data=d)
    if not outdir==None:
        df.to_csv(outdir, sep="\t", index=False)
    return df

def stats_compare(df, col1, col2, test_type):
    """
    Wilcoxon test:
    1. One-sided test: 
        - "greater": df[col1]-df[col2] < 0
        - "less": df[col1]-df[col2] > 0
    2. Two-sided test: 
        - "two-sided": df[col1]-df[col2]=0
    """
    rel=p_value(wilcoxon(df[col1], df[col2], alternative=test_type))  
    return rel


def diagram_compare(df, outdir=None):
    """
    To create boxplot of runningtime for each functions
    """
    boxplot = df.boxplot(column=[c for c in df.columns if c.startswith("T")])
    if not outdir==None:
        plt.savefig(outdir)
        plt.close()

def quick_merge(arr_to_test, time_type, ntest):
    no_quick_faster=0
    no_merge_faster=0
    for i in range(ntest):
        print(i)
        df=collect_data(arr_to_test, time_type)
        rel=stats_compare(df, "T_quick", "T_merge", "two-sided")
        if rel < 0.05:
            rel_greater=stats_compare(df, "T_quick", "T_merge", "greater")
            if rel_greater < 0.05:
                # rel_less=stats_compare(df, "T_quick", "T_merge", "less")
                no_merge_faster+=1
            else:
                no_quick_faster+=1
    return no_quick_faster*100/ntest, no_merge_faster*100/ntest
            
def main():
    n=1000
    arr_to_test="compare_out/arr_to_test_n{}.txt".format(n)
    # generate_arr_to_test(n, arr_to_test)
    t= "process_time"
    # for attempt in range(1,6):
    #     dataout="compare_out/sort_running_time_n{0}_{1}_attempt{2}.txt".format(n, t, attempt)
    #     df=collect_data(arr_to_test, t, dataout)
    #     # df=pd.read_csv("compare_out/sort_running_time_{}_{}.txt".format(n, t), sep="\t")
    #     diaout="dia/sort_running_time_1_{0}_{1}_attempt{2}.png".format(n, t, attempt)
    #     diagram_compare(df, diaout)
    #     d={'T_quick-T_merge': "two-sided"}
    #     print("Attempt no.{}".format(attempt))
    #     for k, v in d.items():
    #         # print(k.split("-"))
    #         rel=stats_compare(df, k.split("-")[0], k.split("-")[1], v)
    #         print("\t", k, "pvalue:", round(rel,4))
    q,m = quick_merge(arr_to_test, t, 500)    
    print("%quickSort() faster: {:.2f}".format(q))
    print("%mergeSort() faster: {:.2f}".format(m))

main()
    
