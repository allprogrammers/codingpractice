##symbol = ['.','+','!']
##    symbol['and'] = '.'
##    symbol['or'] = '|'
##    symbol['not'] = '!'
##    #symbol['brac1'] = '('
##    #symbol['brac2'] = ')'
##    symbol['snot'] = '^' ##kinda supports not operation
class parsetree(object):
    def __init__(self):
        self.top = None
        self.left = None
        self.right = None
premises=input("")    
starter = parsetree()

#always expecting three tokens and always expecting bracket
##def brackfinder(premises):
##    count = 0 
##    for i in premises:
##        if (i =="("):
##            openb.append(count)
##            close.append(" ")
##        elif (i == ")"):
##            closeb.append(count)
##        count += 1

def bracketfinder(tree,premises):
    if (len(premises)==1):
        tree.top = premises
        tree.left = None
        tree.right = None
        print("returned")
        return tree
    elif(premises[0]=="!"):
        tree.top="^"
        tree.left=parsetree()
        tree.left.top="!"
        tree.right = bracketfinder(parsetree(),premises[1:])
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
    tree.top = premises[stop[0]+1]
    print(start[0],stop[0])
    tree.left=bracketfinder(parsetree(),premises[start[0]+1:stop[0]])
    print(start[1],stop[1])
    tree.right=bracketfinder(parsetree(),premises[start[1]+1:stop[1]])
    return tree
            

#def treecreator(tree,premises):
    
##    count=0
##    if (len(premises)==1):
##        print("len is one " + premises)
##        tree.top=premises
##        tree.left = None
##        tree.right = None
##        return tree
##    if (i in symbol):
##        if(i == '!'):
##            print("the value of i is "+ premises[:count] +" " + i +" "+premises[count+1:])
##            tree.top = '!'
##            tree.left=parsetree()
##            tree.left.top= premises[count+1]
##            tree.left.left=None
##            tree.left.right=None
##            tree.right = treecreator(parsetree(),premises[count+2:])
##            break
##        else:
##            print("the value of i is "+ premises[:count] +" " + i +" "+premises[count+1:]) 
##            tree.top = i
##            tree.left = treecreator(parsetree(),premises[:count])
##            tree.right = treecreator(parsetree(),premises[count+1:])
##            break
##    count +=1
##    return tree

starter=bracketfinder(starter,premises)
#depth first search
def dfs(tree,level):
    if (tree.left is not None):
        print("\t"*level+"son")
        dfs(tree.left,level+1)
    print("\t"*level+tree.top)
    if(tree.right is not None):
        print("\t"*level+ "daughter")
        dfs(tree.right,level+1)
dfs(starter,0)
