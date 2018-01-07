def gcd(a,b):
    if a==0:
        return b
    if b==0:
        return a
    return gcd(b,a % b)

for j in range(100,200):
    for i in range(1,100):
        print(gcd(j+i**2,j+(i+1)**2))
