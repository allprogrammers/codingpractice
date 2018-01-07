a=open("map.txt","r")

board = []
for i in a.readlines():
    row = []
    for j in i:
        row.append(j)
    board.append(row)
print (board)
