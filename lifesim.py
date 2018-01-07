a = int(input("How many factors do you think affect your life? "))
b=[]
chofac=[]
for i in range(a):
    factor = input("Please enter factor name: ")
    b.append(factor)
    influence = int(input("Please rate (on scale of 1-9) its influence: "))
    influencetype = input("Is it a good influence or bad influence (g or b): ")
    if(influencetype=="g"):
        k=1
    else:
        k=-1
    l=(i+1)*(k)
    for j in range(influence):
        chofac.append(l)
days = int(input("How many days do you think you will live from now on? "))
bad  = 0
avg = 0
good = 0
import random
e = [0,1]
for i in range(days):
    
    f = random.choice(e)
    if(f):
        d = random.choice(chofac)
        if(d>0):
            good=good+1
        else:
            bad = bad +1
    else:
        avg =avg+1
print(bad,avg,good)
