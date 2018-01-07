#!/bin/python3

import sys
def sublists(lst,d):
    master = []
    for i in range(len(lst)):
        for j in range(i+1,len(lst)):
            newelem = lst[i]+lst[j]
            a,b=(i-1)if i-1 >= 0 else i,(i+1) if i+1 <len(lst) else i 
            if abs(newelem-lst[(i-1)])<=d and abs(newelem-lst[i+1])<=d:
                newlist=lst[:i]+[newelem]+lst[i+1:j]+lst[j+1:]
                master.append(newlist)
    for i in master:
        master += sublists(i,d)
    return master
            
def numberOfLists(s, m, d):
    trivial = [1 for x in range(s)]
    master = [trivial]
    master +=sublists(master[0],d)
    uniq = []
    for i in master:
        if i in uniq:
            continue
        print(i)
        uniq.append(i)
    return len(uniq) % (10**9+9)
    # Complete this function

#  Return the number of lists satisfying the conditions above, modulo 1000000009.
s, m, d = input().strip().split(' ')
s, m, d = [int(s), int(m), int(d)]
result = numberOfLists(s, m, d)
print(result)
