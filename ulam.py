a = 2000
for j in range(2,11):
    lil = [4,5]
    print(lil[-1]-lil[-2])
    for i in range(1,a):
        count = 1
        count2 = 0
        while count < i-count:
            count2 +=1
            #print (i,count,i-count)
            if(count not in lil or (i-count) not in lil):
                count2 -=1
            count +=1
        if(count2 ==1):
            lil.append(i)
            print(lil[-1]-lil[-2],end="")
            #print("ulam ",i)
    #print(lil)
