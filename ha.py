n,q=(int(x) for x in input("").split())
coms = [[i+1] for i in range(n)]
top = []
def merger(query):
    query = query[2:]
    
    a,b = (int(x) for x in query.split())
    #print(a,b,query ,coms)
    firstlist = []
    secondlist = []
    for i in coms:
        for j in i:
            if j == a:
                firstlist = i
            if j == b:
                secondlist = i
    thirdlist = firstlist+secondlist
    #print(firstlist,secondlist,thirdlist)
    coms.remove(firstlist)
    coms.remove(secondlist)
    coms.append(thirdlist)
def size(query):
    #print(query)
    query = query[2:]
    query = int(query)
    for i in coms:
        for j in i:
            if j==query:
                top.append(len(i))

for i in range(q):
    a = input("")
    if (a[0]=="M"):
        merger(a)
    else:
        size(a)
for i in top:
    print(i)
    
