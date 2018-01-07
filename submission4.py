import sys
sys.setrecursionlimit(100000)
def LoadData(filename):
    r = open(filename,'r')
    s = r.readlines()
    toreturn =[]
    for i in range(len(s)):
        a = s[i].strip().split(",")
        toreturn.append((a[0], a[1], a[2], float(a[3]), int(a[4])))
    return toreturn

def selectionSort(lst, col, ascending = True):
    if ascending:
        for j in range(len(lst)):
            minindex = j
            for i in range(j+1,len(lst)):
                if lst[i][col] < lst[minindex][col]:
                    minindex = i
            lst[minindex],lst[j] = lst[j],lst[minindex]
    else:
        for j in range(len(lst)):
            minindex = j
            for i in range(j+1,len(lst)):
                if lst[i][col] > lst[minindex][col]:
                    minindex = i
            lst[minindex],lst[j] = lst[j],lst[minindex]

    return lst

def mergeSort(lst, col, ascending = True):
    if len(lst) <= 1:
        return lst
    mid = len(lst)//2
    left = mergeSort(lst[:mid],col,ascending)
    right = mergeSort(lst[mid:],col,ascending)

    x = []
    i = 0
    j = 0
    if ascending:
        while len(x) < len(left)+len(right):
            if i == len(left):
                x += right[j:]
                break
            if j == len(right):
                x += left[i:]
                break
            if left[i][col] < right[j][col]:
                x += [left[i]]
                i += 1
            else:
                x += [right[j]]
                j += 1
    else:
        while len(x) < len(left)+len(right):
            if i == len(left):
                x += right[j:]
                break
            if j == len(right):
                x += left[i:]
                break
            if left[i][col] > right[j][col]:
                x += [left[i]]
                i += 1
            else:
                x += [right[j]]
                j += 1
    return x

import random
def quicksort(lst,col,ascending=True):
  if ascending == True:
   if len(lst) <= 1:
       return lst
   smaller = []
   greater = []
   partition = random.randint(0,len(lst)-1)
   for i in range(0,len(lst)):
        if i !=partition:
            if lst[i][col] < lst[partition][col]:
                smaller = smaller + [lst[i]]
            else:
                greater = greater + [lst[i]]
   return quicksort(smaller,col,ascending) + [lst[partition]] + quicksort(greater,col,ascending)
  else:
   if len(lst) <= 1:
       return lst
   smaller = []
   greater = []
   partition = random.randint(0,len(lst)-1)
   for i in range(0,len(lst)):
        if i !=partition:
            if lst[i][col] > lst[partition][col]:
                smaller = smaller + [lst[i]]
            else:
                greater = greater + [lst[i]]
   return quicksort(smaller,col,ascending) + [lst[partition]] + quicksort(greater,col,ascending)
