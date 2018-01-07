#tree definition
class parsetree(object):
    def __init__(self):
        self.top = None
        self.left = None
        self.right = None
#inputs premises and conclusion
nop=int(input("Number of premises "))
premises=input("")
nop -=1
for i in range(nop):
    a=input("")
    premises="("+premises+")."+"("+a+")"
    
starter = parsetree()
ctarter = parsetree()
noc=int(input("Number of conclusions "))
conclusion = input("")
noc -=1
for i in range(noc):
    a=input("")
    conclusion="("+conclusion+")."+"("+a+")"
variables = []
#identifies all of the variables
for i in (premises+conclusion):
    if (i.isalpha()):
        if(i in variables):
            continue
        else:
            variables.append(i)
    else:
        continue
#remembers the index of the variable in the truthtable
index = {}
for i in variables:
    index[i]=variables.index(i)
#generates all possible combination of the truthvalues of the variables
truthposs = []
possconst = 2**len(variables)
for i in range(possconst):
    truthposs.append([int(x) for x in bin(i)[2:].zfill(len(variables))])
#stores colum of every variable inside the truthable
truthtable = {}
#print(index)
#print(truthposs)
for i in variables:
    truthtable[i] = []
    truthtable["("+i+")"] = []
    for j in range(possconst):
        #print(i,j,possconst)
        truthtable[i].append(truthposs[j][index[i]])
        truthtable["("+i+")"].append(truthposs[j][index[i]])
        
# parsing function

def bracketfinder(tree,premises):
    if (len(premises)==1):
        tree.top = premises
        tree.left = None
        tree.right = None
        #print("returned")
        return tree
    elif(premises[0]=="!"):
        #print("maagic point",premises)
        tree.top="^"
        tree.left=parsetree()
        tree.left.top="!"
        tree.right = bracketfinder(parsetree(),premises[2:len(premises)-1])
        return tree
    stack = 0
    i=0
    start=[]
    stop=[]
    while (i<len(premises)):
        if (premises[i] == "("):
            if(stack ==0):
                start.append(i)
            stack +=1
        elif (premises[i]==")"):
            stack -=1
            if(stack ==0):
                stop.append(i)
        i +=1
    if(len(start)<2):
        tree.top = premises[start[0]+1:stop[0]]
    else:
        tree.top = premises[stop[0]+1]
        #print("start",tree.top)
        #print(start[0],stop[0])
        tree.left=bracketfinder(parsetree(),premises[start[0]+1:stop[0]])
        #print("left",tree.left.top)
        #print(start[1],stop[1])
        tree.right=bracketfinder(parsetree(),premises[start[1]+1:stop[1]])
        #print("right",tree.right.top)
    return tree

#parses premises and conclusion
starter=bracketfinder(starter,premises)
ctarter=bracketfinder(ctarter,conclusion)

#depth first search to solve the parse tree
stepbystep = []
stepsolver = parsetree()
def solv(tree):
    newtree = parsetree()
    if(tree.top !="^"):
        #print(tree.top)
        newtree.top = "("+tree.left.top+tree.top+tree.right.top+")"
    else:
        newtree.top = "(!"+tree.right.top+")"
    ## old version was stepbystep.append(newtree.top)
    if (not tree.left.top in stepbystep) and tree.left.top !="!":
        stepbystep.append(tree.left.top)
    if not tree.right.top in stepbystep:
        stepbystep.append(tree.right.top)
    st = newtree.top
    #print(newtree.top)
    if(tree.top == "."):
        #tree.left.top AND tree.right.top
        #st=tree.left.top+"."+tree.right.top
        truthtable[st]=[]
        for i in range(possconst):
            b=tree.left.top
            c=tree.right.top
            #print(type(truthtable[b][i]))
            a = truthtable[b][i]*truthtable[c][i]
            truthtable[st].append(a)
    elif(tree.top == "+"):
        #tree.left.top OR tree.right.top
        #st=tree.left.top+"+"+tree.right.top
        truthtable[st]=[]
        for i in range(possconst):
            b=tree.left.top
            c=tree.right.top
            a=0
            if(truthtable[b][i]+truthtable[c][i]):
                a=1
            truthtable[st].append(a)
    elif(tree.top == "^"):
        #NOT tree.right.top
        #st="!"+tree.right.top
        #print("here also")
        truthtable[st]=[]
        for i in range(possconst):
            a= truthtable[tree.right.top][i]^1
            truthtable[st].append(a)
    tree.top = newtree.top
    tree.left = None
    tree.right = None

#tells solv function what to solve 
def enumer(tree):
    if (tree.left is not None):
        #print("\t"*level+"son")
        enumer(tree.left)
            
    #print("\t"*level+tree.top)
    
    if(tree.right is not None):
        #print("\t"*level+ "daughter")
        enumer(tree.right)
    if(tree.top in truthtable):
        #print("treetop",tree.top)
        tree.top = "("+tree.top+")"
        return 1
    elif (tree.top in [".","+","^"]):
        solv(tree)
#print("here you go big son",starter.top)
enumer(starter)
#print("here you go son",ctarter.top)
enumer(ctarter)
gg ="("+premises+")"
bb="("+conclusion+")"
#kind of check whether the parsing and solving were successfull
if(not(gg in truthtable and bb in truthtable)):
    print("parse error")
    exit()
contradiction =0
i=0
#compares the columns of premises and conclusion
counterexamples=[]
while (i<possconst):
    if(truthtable[gg][i]==1):
        if(conclusion in truthtable):
            if(truthtable[conclusion][i]!=1):
                contradiction=1
                counterexamples.append(i)
        else:
            if(truthtable[bb][i]!=1):
                contradiction=1
                counterexamples.append(i)
    i+=1

if(contradiction):
    print("the arguement is false :D")
else:
    print("wow the argument is cool")

count = 97
stepbystep.append(starter.top)
for i in stepbystep:
    print(chr(count),"=",i)
    count +=1


#for i in truthtable:
#    print(chr(count),"=",i)
#    count +=1
for i in range(97,count):
    print("|"+chr(i)+"|",end=" ")
print(possconst)
for j in range(possconst):
    print("",end="\n")
    #print(Fore.RED+"asdfasdf")
    for i in stepbystep:
        print("|"+str(truthtable[i][j])+"|",end=" ")
