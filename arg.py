# assumes brackets are placed where confusion can occur
# take number of premises n
# take n premises
# take number of premises m
# take m conclusions (for now m should be 1)
# identify all of the variables
# create truth table list of lists for all possible values
# create a list answers of conjunctions and disjunctions etc
# final column for all of the premises joined
# comparasion with conclusion with rules of implication
## no code will be removed
## symbols defined are:
### ! for not
### () kind of separators
### . for and
### + for or
symbol = ['.','+','!']
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
conclusion=input("")
variables = []
for i in premises:
    if (i.isalpha()):
        if(i in variables):
            continue
        else:
            variables.append(i)
    else:
        continue
index = {}
for i in variables:
    index[i]=variables.index(i)
truthposs = []
possconst = 2**len(variables)
for i in range(possconst):
    truthposs.append([int(x) for x in bin(i)[2:].zfill(len(variables))])
truthtable = {}
for i in variables:
    truthtable[i] = []
    for j in range(possconst):
        truthtable[i].append(truthposs[index[i]][j])
# parsing starts lol
starter = parsetree()
def treecreator(tree,premises):
    count=0
    if (len(premises)==1):
        tree.top=premises
        tree.left = None
        tree.right = None
        return tree
    for i in premises:
        if (i in symbol):
            if(i == '!'):
                tree.top = '^'
                tree.left = parsetree()
                tree.left.top = '!'
                tree.right = treecreator(parsetree(),premises[count+1:])
            else:
                tree.top = i
                tree.left = treecreator(parsetree(),premises[:count])
                tree.right = treecreator(parsetree(),premises[count+1:])
        count +=1
    return tree
##for i in premises:
##    if (i in symbol):
##        if (i = symbol['not']):
##            working.top=symbol['snot']
##            working.left=
##        """if ( i == symbol['not']):
##            working.top = symbol['snot']
##            working.left = symbol['not']
##            if(premises[count+1]==symbol['brac1']):
##                count2 = count+2
##                for j in premises[count+2:]:
##                    if (j == symbol['brac2']):
##                        break
##                    count2 +=1
##                working.right = premises
##            else:
##                working.right = premises[count + 1]
##        elif (i == symbol['']):
##        elif (i == symbol['']):
##        elif (i == symbol['']):
##        elif (i == symbol['']):
##        elif (i == symbol['']):
##    count +=1"""
## we want to work from bottom up of the tree
