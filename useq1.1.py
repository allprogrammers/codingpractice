
criminals=[]
def newelem(se):
    unii =0
    unij = 0
    posselem = []
    while unii <len(se):
        unij = unii+1
        while unij <len(se):
            if (unii!=unij):
                toa = se[unii]+se[unij]
                #posselem.append(toa)
                if toa in posselem or toa in criminals:
                    if toa in posselem:
                        posselem.remove(toa)
                    if toa not in criminals:
                        criminals.append(toa)
                else:
                    posselem.append(toa)
            unij+=1
        unii+=1
    for i in criminals:
        if i in posselem:
            posselem.remove(i)
    posselem.sort()
    for i in posselem:
        if i>se[-1]:
            return i
def prog(n,k):
    #n,k = (int(x) for x in input("").split())
    seq = [2, 2*n+1]
    i = 2
    while (i<k):
        a= newelem(seq)
        seq.append(a)
        i+=1
    print(seq)
