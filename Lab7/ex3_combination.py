#!/bin/python

import time
from numpy.random import randint
import pandas as pd
import os
import sys
cwd=os.getcwd()
home_dir="/".join(cwd.split("/")[:-1])
sys.path.append(home_dir)
from comparative_test import track_time, p_value
from ex2_sorting_1000 import collect_data, stats_compare, diagram_compare
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


def func0_faster_than_func1(function0, function1, noTest, printCheckpoint=True):
    """
    To check if function 0 is faster than function 1
    """
    func0_faster=0
    n_func0_faster=[0,0] #[n_func0_faster[0], n_func0_faster[1]] is the range of n that function 0 keeps running faster (closed interval)
    # if function0==quickSort:
    #     print(function0([1,3,2], 0, 3))
    d={"T_func0":[], "T_func1": []}
    for n in range(noTest):
        A=[]
        while len(A)<n:
            k=randint(0,n*2)
            if not k in A:
                A.append(k)
        #Track function0
        t_0=0
        count_0=0
        while t_0==0 and count_0<100:
            A_0=[int(i) for i in A]
            if function0 in [insertionSort, heapSort]:
                start_time=time.process_time()
                function0(A_0)
                t_0=time.process_time()-start_time
            elif function0 == quickSort:
                start_time=time.process_time()
                function0(A_0, 0, len(A_0))
                t_0=time.process_time()-start_time
            elif function0 == mergeSort:
                start_time=time.process_time()
                function0(A_0, 0, len(A_0)-1)
                t_0=time.process_time()-start_time
            count_0+=1
        d["T_func0"].append(t_0)
        #Track function1
        t_1=0
        count_1=0
        while t_1==0 and count_1<100:
            A_1=[int(i) for i in A]
            if function1 in [insertionSort, heapSort]:
                start_time=time.process_time()
                function1(A_1)
                t_1=time.process_time()-start_time
            elif function1 == quickSort:
                start_time=time.process_time()
                function1(A_1, 0, len(A_1))
                t_1=time.process_time()-start_time
            elif function1 == mergeSort:
                start_time=time.process_time()
                function1(A_1, 0, len(A_1)-1)
                t_1=time.process_time()-start_time
            count_1+=1
        d["T_func1"].append(t_1)
        if t_0 < t_1:
            if n_func0_faster[1] == 0:
                n_func0_faster[0]=n
                n_func0_faster[1]=n
            else:
                if n_func0_faster[1]==n-1:
                #A of length n-1 mergeSort() is also faster than insertionSort()
                    n_func0_faster[1]=n
                else:
                #Restarting the counter
                    if n_func0_faster[1] - n_func0_faster[0] >=100:
                        if printCheckpoint:
                            print("\tFrom n = {} to {}, {} runs consistently faster than {}".format(n_func0_faster[0], n_func0_faster[1], function0, function1))
                    n_func0_faster=[n,n]
            func0_faster+=1
        #Checkpoint:
        if printCheckpoint:
            if n==100 or n%500==0 and n!=0:
                print("\tFor all n <= {}, percentage of cases that {} is faster than {} is {:.2f}%".format(n, function0, function1, func0_faster/(n+1)*100))
    df=pd.DataFrame(data=d)
    # print(df)
    if printCheckpoint:
        print("\tFrom n = {} to {}, {} runs consistently faster than {}".format(n_func0_faster[0], n_func0_faster[1], function0, function1))
    return n_func0_faster[0]

def func0_faster_than_func1_1(function0, function1, maxTest, time_type, printCheckpoint=True):
    """
    To check if function 0 is faster than function 1
    """
    func0_faster=0
    n_func0_faster=[0,0] #[n_func0_faster[0], n_func0_faster[1]] is the range of n that function 0 keeps running faster (closed interval)
    # if function0==quickSort:
    #     print(function0([1,3,2], 0, 3))
    for n in range(1, maxTest):
        arr=generate_arr_to_test([n])
        d={"T_func0":[], "T_func1": []}
        for i in range(arr.shape[0]):
            A=arr["A"][i]
            #Track function0
            t_0=0
            count_0=0
            while t_0==0 and count_0<100:
                A_0=[int(i) for i in A]
                if function0 in [insertionSort, heapSort]:
                    t_0=track_time(function0(A_0), time_type)
                elif function0 == quickSort:
                    t_0=track_time(function0(A_0, 0, len(A_0)), time_type)
                elif function0 == mergeSort:
                    t_0=track_time(function0(A_0, 0, len(A_0)-1), time_type)
                count_0+=1
            d["T_func0"].append(t_0)
            #Track function1
            t_1=0
            count_1=0
            while t_1==0 and count_1<100:
                A_1=[int(i) for i in A]
                if function1 in [insertionSort, heapSort]:
                    t_1=track_time(function1(A_1), time_type)
                elif function1 == quickSort:
                    t_1=track_time(function1(A_1, 0, len(A_1)), time_type)
                elif function1 == mergeSort:
                    t_1=track_time(function1(A_1, 0, len(A_1)-1), time_type)
                count_1+=1
            d["T_func1"].append(t_1)
        df=pd.DataFrame(data=d)
        # print(df)
        rel=stats_compare(df, "T_func0", "T_func1", "two-sided")
        if rel < 0.05:
            rel_greater=stats_compare(df, "T_func0", "T_func1", "greater")
            if rel_greater < 0.05:
                # rel_less=stats_compare(df, "T_quick", "T_merge", "less")
                continue
            else:
                if n_func0_faster[1] == 0:
                    n_func0_faster[0]=n
                    n_func0_faster[1]=n
                else:
                    if n_func0_faster[1]==n-1:
                        #B of length n-1 mergeSort() is also faster than insertionSort()
                        n_func0_faster[1]=n
                    else:
                        #Restarting the counter
                        if n_func0_faster[1] - n_func0_faster[0] >=50:
                            print("\tFrom n = {} to {}, {} runs consistently faster than {}".format(n_func0_faster[0], n_func0_faster[1], function0, function1))
                        n_func0_faster=[n,n]
                func0_faster+=1
            #Checkpoint:
            if printCheckpoint:
                if n==100 or n%500==0 and n!=0:
                    print("\tFor all n <= {}, percentage of cases that {} is faster than {} is {:.2f}%".format(n, function0, function1, func0_faster/(n+1)*100))
    if printCheckpoint:
        print("\tFrom n = {} to {}, {} runs consistently faster than {}".format(n_func0_faster[0], n_func0_faster[1], function0, function1))
    return n_func0_faster[0]


def main():
    # sizes=[50, 100, 150, 1**3, 10**4]
    # n="_".join([str(n) for n in sizes])
    # arr_to_test=os.path.join(home_dir, "Lab7/compare_out/arr_to_test_n{}.txt".format(n))
    # # generate_arr_to_test(sizes, arr_to_test)
    t="process_time"
    # df=collect_data(arr_to_test, t)
    # attempt=0
    # dia_out="dia/sort_running_time_1_{0}_{1}_attempt{2}.png".format(n, t, attempt)
    # diagram_compare(df,dia_out)
    # rel=stats_compare(df,"greater")
    # print("\tpvalue:", round(rel,4))
    maxsize=100
    print("maxsize:", maxsize)
    for subset in [(mergeSort, insertionSort), (quickSort, mergeSort), (quickSort, insertionSort)]:
    # for subset in [(heapSort, insertionSort)]:
            min_n=[]  
            for i in range(50):
                min_n.append(func0_faster_than_func1(subset[0], subset[1], maxsize, False))
            print(min_n)
            print("\tApproximately n = {}, {} is the faster than {}".format(int(sum(min_n)/len(min_n)), subset[0], subset[1]))
main()


