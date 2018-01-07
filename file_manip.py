file = open("data.txt", "r")
for line in file:
    line = line.strip('\n') #See what happens when we add and remove this line
    data = line.split(' ')
file.close()

print(data)

#converting all the string data into numbers
numbers = []
for i in range(len(data)):
    numbers.append(int(data[i]))

print(numbers)

#finding all the indices of even numbers
indices = []
tup = ()
for i in range(len(numbers)):
    if numbers[i]%2 == 0:
        indices.append(i)
        tup = tup + (i,)    #adding an element to a tuple

print(indices)
print(tup)
