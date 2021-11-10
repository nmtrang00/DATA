#!/bin/python
import math
from numpy.random import randint
import time

def insertionSort(A):
  """
  To implement insertionSort() algorithm
    A:an array of integers.
  O(n^2)
  """
  if len(A)<=1:
    return A
  for i in range(1,len(A)):
    key=A[i]
    j=i-1
    while j >= 0 and A[j] > key:
      A[j+1]=A[j]
      j-=1
    A[j+1]=key
    # print(A)
  return A

def merge(A, start, midpoint, end):
  """
  To implement MERGE() algorithm
    A:an array of integers.
    start: index  to start merging in A (0≤start<len(A))
    midpoint: index dividing the left and right array before merging (start≤midpoint≤end)
    end: index to end merging in A; end is inclusive (0≤end<len(A))
  """
  if A[midpoint] <= A[midpoint+1]:
    #Both A[start:midpoint+1] and A[midpoint+1:end+1] are sorted
    #Then, if the last element in A[start:midpoint+1] is smaller than the first element in A[midpoint+1:end+1], the concatenated array is sorted
    return A
  left=A[start:midpoint+1] #A[midpoint] is included in the left list
  right=A[midpoint+1:end+1]
  left.append(math.inf)
  # print(left)
  right.append(math.inf)
  # print(right)
  i,j=0,0
  for k in range(start,end+1):
    # print(k)
    if left[i] <= right[j]:
      A[k]=left[i]
      i+=1
    else:
      A[k]=right[j]
      j+=1
  return A
# print(merge([2,5,4,7,1,3,2,6],0,math.floor(3/2),3))

def mergeSort(A, start, end):
  """
  To implement mergeSort() algorithm
    A: an array of integers.
    start: index to start mergeSort in A (0≤start<len(A))
    end: index to end  mergeSort  in A; end is inclusive (0≤end<len(A))
  O(nlog(n))
  """
  #end is inclusive
  if len(A) <=1:
    return A
  if start < end:
    midpoint=math.floor((start+end)/2)
    mergeSort(A,start,midpoint)
    mergeSort(A,midpoint+1,end)
    return merge(A, start, midpoint, end)
# print(mergeSort([2,5,4,7,1,3,2,6],0,7))
  
def test(noTest, minValue, maxValue, printCheckpoint=True):
  """
  To check the accuracy of insertionSort() and mergeSort() by comparing 
  results against that from Python sorted() function.
    noTest: number of test to perfrom
    minValue: minimum value of a number in the sequence
    maxValue: maximum value of a number in the sequence
    printCheckpoint: True, if you want to print the percentage of passed test case
      and the percentage of tests that mergeSort() work faster when n reaches checkpoints
  """
  correct=0
  mergeFaster=0
  n_mergeFaster=[0,0] #[n_mergeFaster[0], n_mergeFaset[1]] is the range of nthat mergeSort keeps running faster (closed interval)
  for n in range(noTest):
    B=randint(minValue, maxValue, n)
    B_python=sorted([b for b in B])
    #Run insertion_sort
    start_time_insertion=time.time()
    B_insertion_sort=insertionSort([b for b in B])
    time_insertion=time.time()-start_time_insertion 
    #Run merge sort
    start_time_merge=time.time()
    B_merge_sort=mergeSort([b for b in B],0,len(B)-1)
    time_merge=time.time()-start_time_merge
    if B_python == B_insertion_sort and B_insertion_sort==B_merge_sort:
      correct+=1
    else:
      print("\tTest case #{} failed:".format(n), B)
    if time_merge < time_insertion:
      if n_mergeFaster[1] == 0:
        n_mergeFaster[0]=n
        n_mergeFaster[1]=n+1
      else:
        if n_mergeFaster[1]==n-1:
          #B of length n-1 mergeSort() is also faster than insertionSort()
          n_mergeFaster[1]=n
        else:
          #Restarting the counter
          if n_mergeFaster[1] - n_mergeFaster[0] >=100:
            print("\tFrom n = {} to {}, mergeSort() runs consistently faster than insertionSort()".format(n_mergeFaster[0], n_mergeFaster[1]))
          n_mergeFaster=[n,n]
      mergeFaster+=1
    #Checkpoint:
    if printCheckpoint:
      if n==100 or n%500==0 and n!=0:
        print("\tFor all n <= {}, percentage of cases that mergeSort() is faster than insertionSort() is {:.2f}%".format(n,mergeFaster/(n+1)*100))
  if printCheckpoint:
    print("\tPercentage of cases passed: {:.2f}%".format(correct/noTest*100))
    print("\tFrom n = {} to {}, mergeSort() runs consistently faster than insertionSort()".format(n_mergeFaster[0], n_mergeFaster[1]))
  return n_mergeFaster[0]

def n_merge_faster(noSimulation):
  """
  To estimate the approximate size n of an array that mergeSort() starts
  working faster.
    noSimulation: number of simulation to perform
  """
  min_n=[]
  for i in range(noSimulation):
    min_n.append(test(1000, 0, 10**7, False))
  print(min_n)
  return sum(min_n)/len(min_n)

def main():
  min_n=[]  
  for i in range(1,6):
    print("Attempt no.{}".format(i))
    min_n.append(test(1501, 0, 10**4))
  for i in range(10):
    min_n.append(test(1501, 0, 10**4, False))
  print(min_n)
  print("Approximately n = {}, mergeSort is the faster algorithm based onyour analysis".format(int(sum(min_n)/len(min_n))))
  # test(10**4, 0, 10**7)

# main()
