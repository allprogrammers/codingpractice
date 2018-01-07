positions={"top":0,"middle":1,"bottom":2,"left":0,"right":2}
def getPositions(board,color):
    cords = []
    for r,i in enum(board):
        for c,j in enum(i):
            if j==color:
                cords+=(r,c)
    return cords

def isTouching(board,color1,color2,isTrue=True):
    colorPositions=getPositions(board,color1)
    age_peche = []
    for i in colorPositions:
        age_peche += [(i[0]-1,i[1]),(i[0]+1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1)]
    ylen=len(board)
    xlen=len(board[0])
    for j in age_peche:
        for i in j:
            if i[0]>=0 and i[0]<ylen and i[1]>=0 and i[1]<=ylen:
                if board[i[0]][i[1]] == color2:
                    return not(isTrue)^True
    return not(isTrue)^False

def same(board,color1,color2,parity):
    color1Positions = getPositions(board,color1)
    color2Positions = getPositions(board,color2)

    prev=None
    for i in color1Positions:
        if(i==prev):
            continue
        for j in color2Positions:
            if(i[parity]==j[parity]):
                return True
        prev = i
    return False

def sameRow(board,color1,color2,isTrue=True):
    return not(isTrue)^same(board,color1,color2,0)

def sameColumn(board,color1,color2,isTrue=True):
    return not(isTrue)^same(board,color1,color2,1)

def in(board,pos,color,N,parity):
    color1Positions = getPositions(board,color)
    n=0
    for i in color1Positions:
        if positions[pos]==i[parity]:
            n+=1
    if n>=N:
        return True
    else:
        return False

def inRow(board,pos,color,N,isTrue=True):
    return not(isTrue)^in(board,pos,color,N,0)

def inColumn(board,pos,color,N,isTrue=True):
    return not(isTrue)^in(board,pos,color,N,1)

def isBetween(board,color,betweencol1,betweencol2,isTrue=True):
    bc1Pos = getPositions(board,betweencol1)
    bc2Pos = getPositions(board,betweencol2)
    cPos = getPositions(board,color)
    for i in cPos:
        for j in bc1Pos:
            for k in bc2Pos:
                if (j[0]<i[0] and i[0]<k[0]) or (j[0]>i[0] and i[0]>k[0]) or (j[1]<i[1] and i[1]<k[1]) or (j[1]>i[1] and i[1]>k[1]):
                    return not(isTrue)^True
    return not(isTrue)^False
def atPlace(board,color,row,col,isTrue=True):
    if board[pos[row]][pos[col]]==color:
        return not(isTrue)^True
    return not(isTrue)^False

def isTowards(board,color,direction,color2,isTrue=True):
    dir={"above":(-1,0),"under";(1,0),"right";(0,1),"left":(0,-1)}

    colorPositions = getPositions(board,color)

    for i in colorPositions:
        row = i[0]+dir[direction][0]
        col = i[1]+dir[direction][1]

        while(row>=0 and col >=0):
            if(atPlace(board,color2,row,col)):
                return not(isTrue)^True
            row = i[0]+dir[direction][0]
            col = i[1]+dir[direction][1]
    return not(isTrue)^False

def getColors(colors):
    return colors.split(" ")

def getRules(rules):
    return rules.split("\n")

def inputFromFile(filename):
    filobj = open(filename,"r")
    x=getColors(filobj.readline())
    y=None
    for i in filobj.readlines()[1:]:
       y += (i,)
    return (x,y)

#it doesn't check for the 3x3 exactly
def isValidBoard(board,colors):
    if len(board) != len(board[0]):
        return False
    for i in board:
        for j in i:
            if j not in colors:
                return False
    return True

def checkRules(board,rules):
    functions = {"touch":isTouching,"towards":isTowards,"place":atPlace,"between":inBetween,"row":sameRow,"col":sameColumn,"touches":isTouching}
    for i in rules:
        if i =="":
            continue
        keywords = rules.split(" ")
        if not functions[keywords[0]](keywords[1:]):
            return False


def makePermutations(colors):
    listperm = []
    if len(colors)==1:
        return colors
    for ind,i in enumerate(colors):
        for j in makePermutations(colors[0:ind]+colors[ind+1:]):
            listperm.append(i+" "+j)
    return listperm
