number = input()
count = [0,0,0,0,0,0,0,0,0,0]
for i in number:
    count[int(i)]+=1
print(count.index(max(count)))
