import random

command = open("seq.txt","a")

command.write("to ran\n")
for j in range(0,10):
    #command = open("seq.txt","a")
    #command.write("to ran"+str(j)+"\n")
    for i in range(0,500):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        a=random.choice(["fd","bk"])
        d=random.randint(0, 100)
        c=random.choice(["rt","lt"])
        d=random.randint(0, 30)
        command.write(str(a)+" "+str(d)+" "+str(c)+" "+str(d)+" ")
        command.write("setfloodcolor [random(255) random(255) random(255)] fill ")
    #command.write("\nbitsave \"ran"+str(j)+".bmp\nclearscreen");
    #command.write("\nend\n");
command.write("\nbitsave \"ran"+str(j)+".bmp\nclearscreen");
command.write("\nend\n");
