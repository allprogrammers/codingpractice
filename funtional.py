import turtle
import random

def stars():
    starx = turtle.xcor()
    colortup = (220,220,220)
    while turtle.ycor()>screen.window_height()/2/6:
        turtle.pencolor(colortup)
        starnum = random.randint(1,5)+1
        starcount = 0
        turtle.penup()
        while starcount <= starnum:
            startangle = random.randint(0,90)
            turtle.lt(startangle)
            starsize = random.randint(5,10)
            for i in range(5):
                turtle.fd(starsize)
                turtle.rt(720/5)
            turtle.rt(startangle)
            turtle.penup()
            turtle.setx(turtle.xcor()+random.randint(round(screen.window_width()/starnum)-50,round(screen.window_width()/starnum)+30))
            turtle.pendown()
            starcount +=1
        turtle.penup()
        turtle.sety(turtle.ycor()-50)
        turtle.setx(starx)
        turtle.pendown()
        updown = random.randint(200,255)
        colortup = (updown,updown,updown)

def moon():
    turtle.seth(165)
    colortup = (255,255,255)
    for i in range(170):
        updown = random.randint(200,255)
        colortup= (updown,updown,updown)
        turtle.pencolor(colortup)
        turtle.pensize(round((-(0.1*i-9)**2+85)/5))
        turtle.fd(1)
        turtle.rt(1)

def sea(colortup):
    #turtle.pensize(1)
    #colortup = (colortup[0],colortup[1],colortup[2]-50)
    #turtle.seth(0)
    #while turtle.ycor()>(-1*screen.window_height()/4):
    #    turtle.fd(screen.window_width())
    #    turtle.rt(90)
    #    turtle.fd(1)
    #    turtle.pencolor(colortup)
    #    colortup=(colortup[0],colortup[1],colortup[2]-1)
    #    turtle.rt(90)
    #    turtle.fd(screen.window_width())
    #    turtle.lt(90)
    #    turtle.fd(1)
    #    turtle.pencolor(colortup)
    #    colortup=(colortup[0],colortup[1],colortup[2])
    #    turtle.lt(90)
    pass


def sky():
    colortup = (0,0,25)
    while turtle.ycor()>=60:
        turtle.fd(screen.window_width())
        turtle.rt(90)
        turtle.fd(1)
        turtle.pencolor(colortup)
        colortup=(colortup[0],colortup[1],colortup[2]+1)
        turtle.rt(90)
        turtle.fd(screen.window_width())
        turtle.lt(90)
        turtle.fd(1)
        turtle.pencolor(colortup)
        colortup=(colortup[0],colortup[1],colortup[2])
        turtle.lt(90)
    return colortup

def land():
    pass


screen = turtle.Screen()
turtle.speed("fastest")
turtle.colormode(255)
turtle.penup()
turtle.setx(0-screen.window_width()/2)
turtle.sety(screen.window_height()/2)
turtle.pendown()
colortupfromsky = sky()
turtle.penup()
turtle.setx(40-screen.window_width()/2)
turtle.sety(screen.window_height()/2-40)
turtle.pendown()
turtle.pendown()
stars()
turtle.penup()
turtle.setx(80-screen.window_width()/2)
turtle.sety(screen.window_height()/2-150)
turtle.pendown()
turtle.pendown()
moon()
#turtle.penup()
#turtle.sety(0)
#turtle.setx(0-screen.window_width()/2)
#turtle.pendown()
sea((50,50,50))
#turtle.penup()
#turtle.sety(cord)
#turtle.setx(0-screen.window_width()/2)
#turtle.pendown()
#land()
turtle.done()
