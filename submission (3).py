import time
import random
import sys
sys.setrecursionlimit(1000000)
def LoadData(filename):
    with open(filename,"r") as tor:
        a=tor.readline()
        listtoreturn = []
        while a:
            temptup=a.strip().split(",")
            listtoreturn.append((temptup[0],temptup[1],temptup[2],float(temptup[3]),int(temptup[4])))
            a=tor.readline()
    return listtoreturn

def selectionSort(lst,col,ascending=True):
    for i in range(len(lst)):
        toadd=i
        for j in range(i+1,len(lst)):
            condition = lst[j][col]<lst[toadd][col] if ascending else lst[j][col]>lst[toadd][col]
            if condition:
                toadd=j
        lst[i],lst[toadd]=lst[toadd],lst[i]
    return lst

def mergeSort(lst,col,ascending=True):
    if len(lst)<=1:
        return lst
    left = mergeSort(lst[0:int(len(lst)/2)],col,ascending)
    right = mergeSort(lst[int(len(lst)/2):],col,ascending)
    asorted = []
    i,j=0,0
    while len(asorted)<len(right)+len(left):
        if i < len(right) and j<len(left):
            condition = (right[i][col]<left[j][col]) if ascending else right[i][col]>left[j][col]
            if condition:
                asorted+=[right[i]]
                i+=1
            else:
                asorted+=[left[j]]
                j+=1
        else:
            asorted += right[i:] if i<len(right) else left[j:]
    return asorted

def quicksort(lst,col,ascending=True,first=0,last=-1):
    if len(lst) <= 1:
        return lst
    pivot = random.randint(0,len(lst)-1)
    left = []
    right = []
    for i in range(len(lst)):
        if i!=pivot:
            if (lst[i][col]<=lst[pivot][col]) if ascending else lst[i][col]>=lst[pivot][col]:
                left += [lst[i]]
            else:
                right += [lst[i]]
    return quicksort(left,col,ascending) +[lst[pivot]]+ quicksort(right,col,ascending)

def plotgraphs(lst):
    import matplotlib.pyplot as plt
    times = [[],[],[]]
    for i in range(1000,10001,1000):
        for index,j in enumerate([selectionSort,mergeSort,quicksort]):
            a=time.clock()
            j(lst[:i],4)
            b=time.clock()
            times[index].append(b-a)
    print(times)
    for i in times:
        plt.plot([x for x in range(1000,10001,1000)],i,"ro",linestyle="--")
        plt.show()

plotgraphs(mergeSort(LoadData("books.csv"),4))
#bookslist = LoadData("books.csv")
#plotgraphs(bookslist)
#a = time.clock()
#newlist=mergeSort(bookslist[:],4)
#b = time.clock()
#print(b-a,len(newlist))
##a = time.clock()
##selectionSort(bookslist[:],4)
##b = time.clock()
##print(b-a)
