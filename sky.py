import turtle

screen = turtle.Screen()
turtle.speed("fastest")
turtle.penup()
turtle.setx(0-screen.window_width()/2)
turtle.sety(0)
turtle.pendown()
turtle.colormode(255)
colortup=(255,255,255)
turtle.pencolor(colortup)
while(colortup[0]>=0 and colortup[1]>=0 and colortup[2]>=2):
    turtle.fd(screen.window_width())
    turtle.left(90)
    turtle.fd(1)
    turtle.pencolor(colortup)
    colortup=(colortup[0]-1,colortup[1]-1,colortup[2]-1)
    turtle.left(90)
    turtle.fd(screen.window_width())
    turtle.right(90)
    turtle.fd(1)
    turtle.pencolor(colortup)
    colortup=(colortup[0],colortup[1]-1,colortup[2])
    turtle.right(90)
turtle.done()
