#!/bin/python

import time
import timeit
import numpy as np
from scipy.stats import f

def track_time(function_to_track, type="process_time"):
        """
        To track running time of a function
        """
        if type == "process_time":
            end_time=0
            while end_time==0:
                start_time=time.process_time()
                function_to_track
                end_time= time.process_time()-start_time
            return end_time
        elif type == "time":
            end_time=0
            while end_time==0:
                start_time=time.time()
                function_to_track
                end_time=time.time()-start_time
            return end_time
        elif type == "timeit":
            running_time=timeit.timeit(str(function_to_track), number=5)
            return running_time/5
                
def p_value(rel_stats):
        """
        To format result from scipy.stats
        """
        return float(str(rel_stats).split(",")[1].split(")")[0].split("=")[1])

def F_test(A,B, alternative):
        """
        To calculate F-test
        "one-sided": The variance of 1 sample is not significantly greater than that of another sample
        "two-sided": The variance of 2 samples are not significantly different
        """
        A = np.array(A)
        B = np.array(B)
        deg_of_fredom_A=len(A)-1
        deg_of_fredom_B=len(B)-1
        varA=np.var(A, ddof=deg_of_fredom_A)
        varB=np.var(B, ddof=deg_of_fredom_B)
        if varA/varB >=1:
                F=varA/varB
                dfn=deg_of_fredom_A
                dfd=deg_of_fredom_B
        else:
                F=varB/varA
                dfn=deg_of_fredom_B
                dfd=deg_of_fredom_A
        if alternative=="one-sided":
                p=f.sf(F, dfn, dfd) 
        elif alternative=="two-sided":
                p=f.sf(F, dfn, dfd)*2 
        return p
