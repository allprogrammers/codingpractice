TC = int(input())
bills = []
for i in range(TC):
    n,k = map(int,input().split(" "))
    t=[]
    d=[]
    for j in range(n):
        a,b=map(int,input().split(" "))
        t.append(a)
        d.append(b)
    remaining1=0
    remaining2=0
    for j,l in enumerate(t):
        if k>=l:
            k-=l
        else:
            remaining1 = l-k
            remaining2 = j
            break
    totalcost = 0
    while remaining2 < n:
        totalcost += remaining1*d[remaining2]
        remaining2 +=1
        if remaining2 != n:
            remaining1 = t[remaining2]
    bills.append(totalcost)
for bill in bills:
    print(bill)
