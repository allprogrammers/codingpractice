import random
def merge(left, right,col,ascending=True):
    if not len(left) or not len(right):
        return left or right
    result = []
    i, j = 0, 0
    if ascending:
        while (len(result) < len(left) + len(right)):
            if i == len(left) or j == len(right):
                result=result+left[i:]+right[j:]
                break
            if left[i][col] <= right[j][col]:
                result.append(left[i])
                i+= 1
            else:
                result.append(right[j])
                j+= 1
    else:
        while (len(result) < len(left) + len(right)):
            if i == len(left) or j == len(right):
                result=result+left[i:]+right[j:]
                break
            if left[i][col] >= right[j][col]:
                result.append(left[i])
                i+= 1
            else:
                result.append(right[j])
                j+= 1
    return result

    
def mergeSort (lst, col, ascending=True):
    if len(lst) < 2:
        return lst
    mid = len(lst)//2
    left = mergeSort(lst[:mid],col, ascending)
    right = mergeSort(lst[mid:],col, ascending)
    return merge(left,right,col,ascending)


print(mergeSort([[random.randint(0,100)] for x in range(100)],0,False))
