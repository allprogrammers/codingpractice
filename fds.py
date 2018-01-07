def lastelem(elemlist):
    if len(elemlist) ==1:
        return elemlist[0]
    else:
        return lastelem(elemlist[1:])
def secondlastelem(elemlist):
    if len(elemlist) ==2:
        return elemlist[0]
    else:
        return lastelem(elemlist[1:])
def kthelem(elemlist,k):
    if k==0:
        return elemlist[0]
    else:
        return kthelem(elemlist[1:],k-1)
def reverse(elemlist):
    if len(elemlist) == 1:
        return [elemlist[0]]
    else:
        return reverse(elemlist[1:])+[elemlist[0]]
##def removekthelem(elemlist,k):
##    return elemlist[0:k]+elemlist[k+1:]
##def unique(elem):
##    if elem in removekthelem(elemlist,elem):
##        return False
##    else:
##        return True
##def builder(elemlist):
##    return [x if unique(elemlist[x]) for x in range(0,len(elemlist))]
def unique(elemlist):
    return [elemlist[x] for x in range(0,len(elemlist)) if (not(elemlist[x] in elemlist[x+1:] or elemlist[x] in elemlist[0:x]))]
def maxi(elemlist):
    if len(elemlist)==1:
        return elemlist[0]
    else:
        if elemlist[0]>maxi(elemlist[1:]):
            return elemlist[0]
        else:
            return maxi(elemlist[1:])
def mini(elemlist):
    if len(elemlist)==1:
        return elemlist[0]
    else:
        if elemlist[0]<mini(elemlist[1:]):
            return elemlist[0]
        else:
            return mini(elemlist[1:])
def freq(elemlist):
    return [(x,elemlist.count(x)) for x in elemlist )]
