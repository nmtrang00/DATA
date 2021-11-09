#!/bin/python
import numpy as np
import math
from numpy.random import randint
import time
"""
Below is an example of a square matrix of size n*n:
Square_matrix=[[a_11, a_12... a_1n],
               [a_21, a_22... a_2n]
               ...
               [a_(n-1)1, a_(n-1)2... a_(n-1)n],
               [a_n1, a_n2... a_nn]]
Square_matrix[1][2]=a12
Square_matrix_np=np.array(Square_matrix)
Square_matrix_np[1,2]=Square_matrix[1][2]
In Strassen's algorithm, it is assumed that n is an exact power of 2.
"""
def split_matrices(X, mid):
    """
    To split a square matrix of size (n,n), into 4 submatrices of size (n/2,n/2) using list comprehension
        X: A square matrix of size (n,n) (n=2**i, i>0)
        mid: The midpoint to devide X (0< mid <n/2)
    """
    X11=[[X[r][c] for c in range(mid)] for r in range(mid)]
    X12=[[X[r][c] for c in range(mid,len(X))] for r in range(mid)]
    X21=[[X[r][c] for c in range(mid)] for r in range(mid,len(X))]
    X22=[[X[r][c] for c in range(mid,len(X))] for r in range(mid,len(X))]
    return X11, X12, X21, X22

def add(Y,Z):
    """
    To calculate sum of 2 square matrices Y+Z
        Y: a square matrix of size (n,n)
        Z: a square matrix of size (n,n) 
        n>=0
    """
    return [[Y[r][c] + Z[r][c]  for c in range(len(Y))] for r in range(len(Y))]

def subtract(Y,Z):
    """
    To calculate difference of 2 square matrices Y-Z
        Y: a square matrix of size (n,n)
        Z: a square matrix of size (n,n) 
        n>=0
    """
    return [[Y[r][c] - Z[r][c]  for c in range(len(Y))] for r in range(len(Y))]

def Strassen(A, B):
    """
    To implement Strassen algorithm when splitting matrices with Python list comprehension
        A: a square matrix of size (n,n) (n=2**i, i>=0)
        B: a square matrix of size (n,n) (n=2**i, i>=0)
    """
    n=len(A)
    # print(n)
    C=[[0]*n]*n
    # print(C)
    if n==0:
        return C
    elif n<=1:
        C[0][0]=A[0][0]*B[0][0]
    else:
        #Split matrices
        mid=int(n/2) 
        A11,A12,A21,A22=split_matrices(A,mid)
        B11,B12,B21,B22=split_matrices(B,mid)

        #Create sum and difference matrices
        S1=subtract(B12,B22)
        S2=add(A11,A12)
        S3=add(A21,A22)
        S4=subtract(B21,B11)
        S5=add(A11,A22)
        S6=add(B11,B22)
        S7=subtract(A12,A22)
        S8=add(B21,B22)
        S9=subtract(A11,A21)
        S10=add(B11,B12)

        #Create product of sum matrices
        P1=Strassen(A11,S1)
        P2=Strassen(S2,B22)
        P3=Strassen(S3,B11)
        P4=Strassen(A22,S4)
        P5=Strassen(S5,S6)
        P6=Strassen(S7,S8)
        P7=Strassen(S9,S10)

        #Compute final C
        C11=subtract(add(add(P5,P4),P6),P2) #C11=P5+P4-P2+P6=((P5+P4)+P6)-P2
        C12=add(P1,P2)
        C21=add(P3,P4)
        C22=subtract(add(P5,P1),add(P3,P7)) #C22=P5+P1-P3-P7=P5+P1-(P3+P7)

        # Combine back to C
        [C11[r].extend(C12[r]) for r in range(len(C11))]
        [C21[r].extend(C22[r]) for r in range(len(C21))]
        C11.extend(C21)
        C=C11
    return C

def split_matrices_use_numpy(X,mid):
    """
    To split a square matrix of size (n,n), into 4 submatrices of size (n/2,n/2) using numpy matrix indices
        X: A square matrix of size (n,n) (n=2**i, i>0)
        mid: The midpoint to devide X (0< mid <n/2)
    """
    return X[0:mid, 0:mid], X[0:mid, mid:], X[mid:, 0:mid], X[mid:, mid:]

def Strassen_use_numpy_matrices(A, B):
    """
    To implement Strassen algorithm when splitting matrices with numpy matrix indices
        A: a square matrix of size (n,n) (n=2**i, i>=0)
        B: a square matrix of size (n,n) (n=2**i, i>=0)
    """
    n,n=A.shape
    C=np.zeros((n,n))

    if n==0:
        return C
    elif n==1:
        C[0,0]=A[0,0]*B[0,0]
    else:
        #Split matrices
        mid=int(n/2) 
        A11,A12,A21,A22=split_matrices_use_numpy(A,mid)
        B11,B12,B21,B22=split_matrices_use_numpy(B,mid)

        #Create sum and difference matrices
        S1=B12-B22
        S2=A11+A12
        S3=A21+A22
        S4=B21-B11
        S5=A11+A22
        S6=B11+B22
        S7=A12-A22
        S8=B21+B22
        S9=A11-A21
        S10=B11+B12

        #Create product of sum matrices
        P1=Strassen_use_numpy_matrices(A11,S1)
        P2=Strassen_use_numpy_matrices(S2,B22)
        P3=Strassen_use_numpy_matrices(S3,B11)
        P4=Strassen_use_numpy_matrices(A22,S4)
        P5=Strassen_use_numpy_matrices(S5,S6)
        P6=Strassen_use_numpy_matrices(S7,S8)
        P7=Strassen_use_numpy_matrices(S9,S10)

        #Compute final C
        C11=P5+P4-P2+P6
        C12=P1+P2
        C21=P3+P4
        C22=P5+P1-P3-P7

        # Combine back to C
        C1=np.hstack((C11,C12))
        C2=np.hstack((C21,C22))
        C=np.vstack((C1,C2))
    return C

def test_runtime_split(n):
    """
    To test the runtime of split function using Python list comprehension
    and numpy matrix indices
        n: Number of row/col in the matrix to be tested (n=2i, i>0)
    """
    A=randint(n**2, size=(n, n))
    start_split=time.time()
    split_matrices(A,int(len(A)/2))
    print("CPU time of split_matrices(): {}".format(time.time()-start_split))
    start_split_use_numpy=time.time()
    split_matrices_use_numpy(A,int(len(A)/2))
    print("CPU time of split_matrices_use_numpy(): {}".format(time.time()-start_split_use_numpy))

def single_test_case():
    """
    A specific test to see results from 3 function np.dot, Strassen() and Strassen_use_numpy_matrices()
    """
    A=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    B=[[13,14,15,16],[9,10,11,12],[5,6,7,8],[1,2,3,4]]
    print(np.dot(np.array(A),np.array(B)))
    print(np.array(Strassen(A,B)))
    print(Strassen_use_numpy_matrices(np.array(A),np.array(B)))

def multiple_test_cases(noTest):
    """
    To test the accuracy of Strassen() and Strassen_use_numpy_matrices(), 
    by comparing results again one from np.dot().
    noTest: number of test to perform
    """
    count=0
    for i in range(noTest):
        n=2**randint(0,4)
        A=randint(10, size=(n, n))
        B=randint(10, size=(n, n))
        C_np_dot=np.dot(A,B)
        C_Strassen=np.array(Strassen(A,B))
        C_Strassen_use_numpy_matrices=Strassen_use_numpy_matrices(A,B)
        if np.sum(C_Strassen_use_numpy_matrices-C_np_dot)==0 and np.sum(C_Strassen-C_Strassen_use_numpy_matrices)==0:
            count+=1
        else:
            print("Test case no.{} failed:".format(n))
            print(A,B,sep="\n")
            print("Expected result from np.dot:",C_np_dot,sep="\n")
            print("Result from Strassen():",C_Strassen,sep="\n")
            print("Result from Strassen_use_numpy_matrices():",C_Strassen_use_numpy_matrices,sep="\n")
    print("Percentage of test cases passed: {:.2f}%".format(count/noTest*100))

def main():
    test_runtime_split(10)
    # single_test_case()
    multiple_test_cases(100)
main()