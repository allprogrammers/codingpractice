import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def addEdges(G,lst):
    G.add_edges_from(lst)
    return G

def listOfNodes(G):
    return G.nodes()

def listOfEdges(G):
    return G.edges()

def adjacencyMatrix(G):
    A = nx.to_numpy_matrix(G)
    return A

def adjacencyList(G):
    a = {}
    for i in listOfNodes(G):
        a[i] = G.neighbors(i)
    return a

def printNeighboursAndDegrees(G):
    aList = adjacencyList(G)
    for i in aList.keys():
        print(len(aList[i]),aList[i])

def drawGraph(G):
    pos1 = nx.spring_layout(G)
    nx.draw(G,pos=pos1,with_labels=True)
    elabels = nx.draw_networkx_edge_labels(G,pos1)
    plt.show()

def printInDegreeOutDegree(G):
    n=listOfNodes(G)
    for i in n:
        print(i,G.in_degree(i),G,out_degree(i))
    #e=listOfEdges(G)
    #for i in n:
    #    incount = 0
    #    outcount = 0
    #    for j in e:
    #        if j[0]==i:
    #            outcount +=1
    #        if j[1]==i:
    #            incount +=1
    #    print(i,incount,outcount)

def addWeightedEdges(G,lst):
    for i in lst:
        G.add_edge(i[0],i[1],{'weight':i[3]})

def sumInDegrees(G):
    n = listOfNodes(G)
    sumin = 0
    for i in n:
        sumin += G.in_degree(i)
    return sumin

def sumOutDegrees(G):
    n = listOfNodes(G)
    sumout = 0
    for i in n:
        sumout += G.out_degree(i)
    return sumout

def sumEdges(G):
    return G.number_of_edges()

def compareDegreesAndEdges(G):
    if sumInDegrees(G) == sumOutDegrees(G) == sumEdges(G)/2:
        return True
    return False

def graphDiameter(G):
    return nx.diameter(G)

def graphDensity(G):
    return nx.density(G)

#def Question1():
#    G=nx.Graph()
#    G.add_edges_from([(1,2),(1,5),(2,5),(2,4),(2,3),(3,4),(4,5)])
#    print(listOfNodes(G))
#    print(listOfEdges(G))
#    print(adjacencyMatrix(G))
#    print(adjacencyList(G))
#    printNeighbourAndDegrees(G)
#
#def Question2():
#    G=nx.DiGraph()
#    G.add_edges_from([(1,2),(2,4),(3,1),(3,2),(4,3),(4,4)])
#    drawGraph(G)
#    print(adjacencyMatrix(G))
#    print(adjacencyList(G))
#    printInDegreeOutDegree(G)
#
#def Question3():
#    G=nx.DiGraph()
#    G.add_edges_from([("Dallas","Austin"),("Dallas","Denver"),("Dallas","Chicago"),("Austin","Dallas"),("Austin","Houston"),("Chicago","Denver"),("Houston","Atlanta"),("Atlanta","Washington"),("Washington","Atlanta"),("Washington","Dallas"),("Denver","Atlanta"),("Denver","Chicago")])
#    printInDegreeOutDegree(G)
#    print(compareDegreesAndEdges(G))
#    print(graphDiameter(G))
#    print(graphDensity(G))
#
#def Question4():
#    G= nx.Graph()
#    addEdges(G,[("a","b")("a","d"),("b","e"),("b","c"),("c","e"),("e","d")])
#    addEdges(G,[("a","b"),("d","b"),("f","c"),("b","f"),("b","c")])
#    drawGraph(G1)
#    print(listOfNodes(G))
#    print(listOfEdges(G))
#    print(adjacencyMatrix(G))
#    print(adjacencyList(G))
#
def LoadDataIntoGraph(filename):
    tor = open(filename,"r").read()
    data = [x.split(",") for x in tor.split("\n")]
    G = nx.Graph()
    for i in range(1,len(data)):
        for j in range(1,len(data[i])):
            if data[i][j]!="-1":
                G.add_edge(data[i][0],data[0][j],{"weight":data[i][j]})
    return G

def Question5():
    G=LoadDataIntoGraph("connections.csv")
    drawGraph(G)
    print(listOfNodes(G))
    print(listOfEdges(G))
    print(adjacencyMatrix(G))
    print(adjacencyList(G))
    printNeighboursAndDegrees(G)
Question5()

def reverseString(reverseMe):
    newString = ""
    while reverseMe:
        newString += reverseMe[-1]
        reverseMe = reverseMe[:-1]
    return newString

def checkRoundPBalance(exp):
    stack = []
    for i in exp:
        if i=="(":
            stack.append(i)
        elif i==")":
            if len(stack) !=0:
                temp = stack.pop()
                continue
            else:
                return False
    if stack:
        return False
    return True

def checkRoundCurlyPBalance(exp):
    stack = []
    opclose = {")":"(","}":"{"}
    rev = {a:b for b,a in opclose.items()}
    for i in exp:
        if i in rev.keys():
            stack.append(i)
        elif i in opclose.keys():
            if len(stack) !=0 and stack.pop() == opclose[i]:
                    continue
            else:
                return False
    if stack:
        return False
    return True

def postfixEval(exp):
    exp2 = exp.split(" ")
    exp2.reverse()
    stack = []
    while exp2:
        a=exp2[-1]
        exp2 = exp2[:-1]
        while a not in ["+","-","/","*"]:
            stack.append(a)
            a=exp2[-1]
            exp2 = exp2[:-1]
        else:
            k,b=float(stack.pop()),float(stack.pop())
            posans={"+":k+b,"-":b-k,"/":b/k,"*":k*b}
            stack.append(posans[a])
    return stack.pop()


#print(checkRoundCurlyPBalance("{(})"))
#G = nx.Graph()
#print("asafd")
#G.add_nodes_from([1,2,3,4,5])
#print("asafd")
#addEdges(G,[(1,2),(2,3),(2,4)])
#print("asafd")
#drawGraph(G)
#print("asafd")
