positions={"top":0,"middle":1,"bottom":2,"left":0,"right":2}
def getPositions(board,color):
    cords = []
    for r,i in enumerate(board):
        for c,j in enumerate(i):
            if j==color:
                cords.append((r,c))
    return cords

def isTouching(board,color1,color2,isTrue=True):
    colorPositions=getPositions(board,color1)
    age_peche = []
    ylen=len(board)
    xlen=len(board[0])
    for i in colorPositions:
        age_peche = [(i[0]-1,i[1]),(i[0]+1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1)]
        for j in age_peche:
            if j[0]>=0 and j[0]<ylen and j[1]>=0 and j[1]<xlen:
                if board[j[0]][j[1]] == color2:
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

def infunc(board,pos,color,N,parity):
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
    return not(isTrue)^infunc(board,pos,color,N,0)

def inColumn(board,pos,color,N,isTrue=True):
    return not(isTrue)^infunc(board,pos,color,N,1)

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
    if board[positions[row]][positions[col]]==color:
        return not(isTrue)^True
    return not(isTrue)^False

def isTowards(board,color,direction,color2,isTrue=True):
    dire={"above":(1,0),"under":(-1,0),"bottom":(-1,0),"below":(-1,0),"right":(0,-1),"left":(0,1)}

    colorPositions = getPositions(board,color)

    for i in colorPositions:
        row = i[0]+dire[direction][0]
        col = i[1]+dire[direction][1]
        height=len(board)
        width=len(board[0])

        while(row>=0 and col >=0) and (row<height and col<width):
            if(board[row][col]==color2):
                return not(isTrue)^True
            row +=dire[direction][0]
            col +=dire[direction][1]
    return not(isTrue)^False

def getColors(colors):
    return [x.strip("\n") for x in colors.split(" ")]

def getRules(rules):
    rules2return = []
    for i in rules.split('\n'):
        if i!="":
            rules2return.append(i)
    return rules2return

def inputFromFile(filename):
    filobj = open(filename,"r")
    x=getColors(filobj.readline())
    y=[]
    for i in filobj.readlines()[1:]:
        rule =i.strip("\n")
        if rule!="":
           y += (i.strip("\n"),)
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

def checkRuless(board,rules):
    for i in rules:
        keywords=i.split(" ")
        if(keywords[0]=="touch" or keywords[0]=="touches"):
            tbool=True
            if len(keywords)==4 and keywords[3]=="not":
                tbool=False
            if not isTouching(board,keywords[1],keywords[2],tbool):
                return False
        if(keywords[0]=="towards"):
            tbool=True
            if len(keywords)==5 and keywords[4]=="not":
                tbool=False
            if not isTowards(board,keywords[1],keywords[2],keywords[3],tbool):
                return False
        if(keywords[0]=="place"):
            tbool=True
            if len(keywords)==4 and keywords[3]=="not":
                tbool=False
            if "." in keywords[2]:
                posone,postwo = keywords[2].split(".")
            else:
                posone=keywords[2]
                postwo=keywords[2]
            if not atPlace(board,keywords[1],posone,postwo,tbool):
                return False
        if(keywords[0]=="between"):
            tbool=True
            if len(keywords)==5 and keywords[4]=="not":
                tbool=False
            if not isBetween(board,keywords[1],keywords[2],keywords[3],tbool):
                return False
        if(keywords[0]=="row"):
            tbool=True
            if len(keywords)==5 and keywords[4]=="not":
                tbool=False
            if not inRow(board,keywords[3],keywords[1],int(keywords[2]),tbool):
                return False
        if(keywords[0]=="col"):
            tbool=True
            if len(keywords)==5 and keywords[4]=="not":
                tbool=False
            if not inColumn(board,keywords[3],keywords[1],int(keywords[2]),tbool):
                return False
        if(keywords[0]=="samerow"):
            tbool=True
            if len(keywords)==4 and keywords[3]=='not':
                tbool=False
            if not sameRow(board,keywords[1],keywords[2],tbool):
                return False
        if(keywords[0]=="samecolumn"):
            tbool=True
            if len(keywords)==4 and keywords[3]=='not':
                tbool=False
            if not sameColumn(board,keywords[1],keywords[2],tbool):
                return False
    return True

def checkRules(board,rules,isTrue=True):
    return not(isTrue)^checkRuless(board,rules)

def makePermutations(colors):
    #returns permutations

def GameSolver(filename):
    x,y=inputFromFile(filename)
    print(x,y)
    for i in makePermutations(x):
        boardpass=[[i[0],i[1],i[2]],[i[3],i[4],i[5]],[i[6],i[7],i[8]]]
        if checkRules(boardpass,y):
            return boardpass
    return []
