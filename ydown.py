from subprocess import call
import os
count=open("downloaded.txt","a")
ter=1
with open("youtube.txt","r") as f:
    for line in f:
        os.system("youtube-dl -f 140 "+line)
        #call(["youtube-dl","\"https://www.youtube.com/watch?v=TAhyZegVkhw\""])
        count.write(str(ter)+"\n")
        ter = ter+1
