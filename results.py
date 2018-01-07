from bs4 import BeautifulSoup
import urllib.request

dump = open("results.html","a")
number = open("number.txt","r")
k=int(number.readlines()[0])
print(k)
print("nice")
for i in range(k,99999999,600):
    number1 = open("number.txt","w")
    number1.write(str(i))
    url = "https://ugadmissions.nust.edu.pk/result/meritresult.aspx?rn="+str(i)
    soupfile2 = urllib.request.urlopen(url)
    soupfile = soupfile2.read()
    soup = BeautifulSoup(soupfile,"html5lib")
    condump = soup.find("div",{"id":"main-container-body"})
    dump.write("\n"+str(condump))
