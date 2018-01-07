import random


graph = open("graphcom.txt","w")
for j in range(0,50):
    graph.write("to ran"+str(j)+"\n")
    for i in range(0,100):
        a=random.randint(0,100)
        b=random.choice(["fd","bk"])
        graph.write(b)
        c=""
        if (b=="fd"):
            c=" bk "
        else:
            c=" fd "
        graph.write(" "+str(a)+c+str(a)+" rt 90 fd 4 lt 90 ")
    graph.write("\nbitsave \"ran"+str(j)+".bmp\nclearscreen\nend\n")
