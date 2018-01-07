import random

for j in range(0,50):
    command = open("seq.txt","a+")
    command.write("to ran"+str(j)+"\n")
    for i in range(0,5000):
        a=random.choice(["fd","bk"])
        b=random.randint(0, 10)
        c=random.choice(["rt","lt"])
        d=random.randint(0, 180)
        command.write(str(a)+" "+str(b)+" "+str(c)+" "+str(d)+" ")
    command.write("\nbitsave \"ran"+str(j)+".bmp\nclearscreen");
    command.write("\nend\n");
