def oed(n,k):
    if k==1:
        return 0 if n%2 ==1 else n
    firstdigit = n//(10**(k-1))
    remaining = n-firstdigit*(10**(k-1))
    ans = 0 if (firstdigit%2==1) else firstdigit
    part2 = oed(remaining,k-1)
    n,temp = 0,part2//10
    while temp>9:
        temp = temp//10
        n+=1
    a= ans*(10**n)+part2
    return a

print(oed(23265,5))
