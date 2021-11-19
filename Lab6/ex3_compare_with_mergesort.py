#!/bin/python
import time
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import wilcoxon, ttest_ind
from numpy.random import randint
import numpy as np
import seaborn as sns
import os
import sys
from ex2_heapsort import heapSort
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value, F_test
sys.path.append(os.path.join(home_dir, "Lab2"))
from ex3_insertion_sort_merge_sort import mergeSort

"""
Both runs in O(nlog(n))
"""
def generate_arr_to_test(sizes, outdir):
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
    df.to_csv(outdir, index=False, sep="\t")

def collect_data(arr_to_test, time_type, outdir=None):
    """
    To track runningtime of 2 sorting functions
    """
    arr=pd.read_csv(arr_to_test, sep="\t", header=0)
    d={"T_merge": [], "T_heap": []}
    for i in range(arr.shape[0]):
        A=arr["A"][i][1:len(arr["A"][i])-1].split(",")
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

def stats_compare(df, test_type):
    """
    Wilcoxon test:
    1. One-sided test: 
        - "greater": df[col1]-df[col2] < 0
        - "less": df[col1]-df[col2] > 0
    2. Two-sided test: 
        - "two-sided": df[col1]-df[col2]=0
    """
    rel=p_value(wilcoxon(df["T_merge"], df["T_heap"], alternative=test_type))  
    return rel


def diagram_compare(df, outdir=None):
    """
    To create boxplot of runningtime for each functions
    """
    boxplot = df.boxplot(column=[c for c in df.columns if c.startswith("T")])
    if not outdir==None:
        plt.savefig(outdir)
        plt.close()
    
    
def main():
    sizes_0=[15,50,100,1000]
    # sizes=[sizes_0[0]]
    sizes=sizes_0[:]
    n="_".join([str(n) for n in sizes])
    arr_to_test="compare_out/arr_to_test_n{}.txt".format(n)
    # generate_arr_to_test(sizes, arr_to_test)
    t="process_time"
    # for attempt in range(1,6):
    #     dataout="compare_out/sort_running_time_n{0}_{1}_attempt{2}.txt".format(n, t, attempt)
    #     df=collect_data(arr_to_test, t, dataout)
    #     # df=pd.read_csv("compare_out/sort_running_time_{}_{}.txt".format(n, t), sep="\t")
    #     diaout="dia/sort_running_time_{0}_{1}_attempt{2}.png".format(n, t, attempt)
    #     diagram_compare(df, diaout)
    #     print("Attempt no.{}".format(attempt))
    #     rel=stats_compare(df,"greater")
    #     print("\tpvalue:", round(rel,4))
    df=collect_data(arr_to_test, t)
    diagram_compare(df)
    rel=stats_compare(df,"greater")
    print("\tpvalue:", round(rel,4))
    
    
main()




