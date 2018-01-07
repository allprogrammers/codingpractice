import random

command = open("seq.txt","a")
for k in range(0,10):
    command.write("to ran"+str(k)+"\nrt 90")
    for j in range(0,300):
        #command = open("seq.txt","a")
        #command.write("to ran"+str(j)+"\n")
        som=0
        while(som!=300):
            r=random.randint(0,255)
            g=random.randint(0,255)
            b=random.randint(0,255)
            l=random.randint(0,300-som)
            som = som+ l
            
            command.write(" setpensize ["+str(random.randint(1,10))+" "+str(random.randint(1,10))+"] fd "+str(l)+" "+"setpc ["+str(r)+" "+str(g)+" "+str(b)+"] ")
        if (j%2):
            command.write("rt 90 fd 1 rt 90 ")
        else:
            command.write("lt 90 fd 1 lt 90 ")
        command.write(random.choice(["rt ","lt "])+str(random.randint(0,30))+" ")
    command.write("\nbitsave \"ran"+str(k)+".bmp\nclearscreen\nend\n")
