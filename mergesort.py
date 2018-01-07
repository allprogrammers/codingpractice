def mergesort(lst):
    if len(lst)<=1:
        return lst
    left = mergesort(lst[0:int(len(lst)/2)])
    right = mergesort(lst[int(len(lst)/2):])
    asorted = []
    i,j=0,0
    while len(asorted)<len(right)+len(left):
        if i < len(right) and j<len(left):
            if right[i]<left[j]:
                asorted+=[right[i]]
                i+=1
            else:
                asorted+=[left[j]]
                j+=1
        else:
            asorted += right[i:] if i<len(right) else left[j:]
    return asorted
