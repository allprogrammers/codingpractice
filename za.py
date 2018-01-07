height= int (input ("enter the height"))
c= height+1
for line in range (height):
    spacenumber=c-( c-(height-line))
    starnumber= c-(c-(c-line-1))
    print (spacenumber * " " + starnumber* "* ")


