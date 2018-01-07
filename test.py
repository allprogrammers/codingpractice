#!/bin/python3

import sys


n = int(input().strip())
a = input().split()
s = [int (x) for x in a]
mistakes=0
if (not(s[0]==1)):
    mistake +=1
if (n<1 or n > 10**3):
    print("error")
    exit()
count=1
while (count < len(s)):
    if(s[count] < 1 or s[count]>10**3):
        print("error")
        exit()
    else:
        if(not(s[count]==s[count-1]+1)):
           mistakes +=1
           #print("a")
    count +=1
print (mistakes)


irow=a
icol=b
rowconst = [0,a]
colconst = [0,m]
kon = 1
kon2 =1
