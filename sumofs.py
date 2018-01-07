import turtle

n=10
turtle.speed("fastest")
for i in range(100):
    for j in range(4):
        turtle.fd(10*i)
        turtle.left(90)
    turtle.fd(10*i)
    turtle.left(180)
turtle.done()
