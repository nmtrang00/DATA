#!/bin/bash
from numpy.random import randint
from scipy.stats import wilcoxon
import pandas as pd
import os
import sys
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
from ex2_sorting_1000 import diagram_compare
from ex1_quick_sort import quickSort
sys.path.append(os.path.join(home_dir, "Lab2"))
from ex3_insertion_sort_merge_sort import insertionSort, mergeSort
sys.path.append(os.path.join(home_dir, "Lab6"))
from ex2_heapsort import heapSort

"""
Time complexity:
quickSort(): O(n^2) worst case, O(nlog(n)) avg case
mergeSort(): O(nlog(n))
heapSort(): O(nlog(n))
insertionSort(): O(n^2)
Expectation: T_insertion > T_quick ~ T_merge ~ T_heap
"""
def combination_sort(A):
    if len(A) in [0, 1]:
        return A
    elif len(A) in range(2,91):
        return insertionSort(A)
    elif len(A) in range(91, 500):
        return mergeSort(A, 0, len(A)-1)
    else:
        return quickSort(A, 0, len(A))

def combination_sort_v1(A):
    if len(A) in [0, 1]:
        return A
    elif len(A) in range(2,50):
        return insertionSort(A)
    else:
        return quickSort(A, 0, len(A))

def generate_arr_to_test(sizes, outdir=None):
    df=pd.DataFrame()
    arr=[]
    testSizes=sizes[:]
    for i in range(100):
        testSizes.extend(sizes)
    for n in testSizes:
        A=[]
        while len(A)<n:
            k=randint(0,n*2)
            if not k in A:
                A.append(k)
        arr.append(A)
    df["A"]=arr
    # print(df)
    if not outdir==None:
        df.to_csv(outdir, index=False, sep="\t")
    return df

def collect_data(arr_to_test, time_type, outdir=None):
    """
    To track runningtime of 4 sorting functions
    """
    arr=pd.read_csv(arr_to_test, sep="\t", header=0)
    d={ "T_insertion":[], "T_quick": [], "T_merge": [], "T_heap": [], "T_combination": []}
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
        t_c=0
        count_c=0
        while t_c==0 and count_c<100:
            A_combination=[int(i) for i in A]
            t_c=track_time(combination_sort_v1(A_combination))
            count_c+=1
        d["T_combination"].append(t_c)
    df=pd.DataFrame(data=d)
    if not outdir==None:
        df.to_csv(outdir, sep="\t", index=False)
    return df

def stats_compare(df):
    """
    Wilcoxon test:
    1. One-sided test: 
        - "greater": df[col1]-df[col2] < 0
        - "less": df[col1]-df[col2] > 0
    2. Two-sided test: 
        - "two-sided": df[col1]-df[col2]=0
    """
    rel={ "T_insertion":[], "T_quick": [], "T_merge": [], "T_heap": []}
    for col2 in rel.keys():
        rel[col2]=p_value(wilcoxon(df["T_combination"], df[col2], alternative="greater"))
    return rel

def main():
    # A=[]
    # n=100
    # while len(A)<n:
    #     k=randint(0,n*2)
    #     if not k in A:
    #         A.append(k)
    # print(combination_sort(A))
    sizes=[50, 100, 500, 1000, 10000]
    # sizes=[sizes_0[0]]
    # sizes=sizes_0
    for attempt in range(1,6):
        print("Attempt no.{}".format(attempt))
        n="_".join([str(n) for n in sizes])
        arr_to_test=os.path.join(home_dir, "Lab7/compare_out/arr_to_test_n{}_attempt{}.txt".format(n, attempt))
        generate_arr_to_test(sizes, arr_to_test)
        print("Done generating data")
        t="process_time"
        outdir="compare_out/running_time_combination_n{}_attempt{}_v1.txt".format(n, attempt)
        df=collect_data(arr_to_test, t, outdir)
        dia_out="dia/sort_running_time_1_{0}_{1}_attempt{2}_v1.png".format(n, t, attempt)
        diagram_compare(df,dia_out)
        df=pd.read_csv(outdir,sep="\t")
        rel=stats_compare(df)
        print("\tn:", n)
        for k,v in rel.items():
            print("\t\t{} pvalue: {:.4f}".format(k, v))

main()