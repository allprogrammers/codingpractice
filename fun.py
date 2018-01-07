import pylab as pl
from scipy.misc import imresize, imfilter
import turtle

# load image
img = pl.flipud(pl.imread("face.png"))

# setup turtle
levels = 8
size = 2**levels
turtle.setup(img.shape[1] * 4.2, img.shape[0] * 4.2)
turtle.setworldcoordinates(0, 0, size, -size)
turtle.tracer(1000, 0)

# resize and blur image
img = imfilter(imresize(img, (size, size)), 'blur')

# define recursive hilbert curve
def hilbert(level, angle = 90):
    if level == 0:
        return
    if level == 1 and img[-turtle.pos()[1], turtle.pos()[0]] > 128:
        turtle.forward(2**level - 1)
    else:
        turtle.right(angle)
        hilbert(level - 1, -angle)
        turtle.forward(1)
        turtle.left(angle)
        hilbert(level - 1, angle)
        turtle.forward(1)
        hilbert(level - 1, angle)
        turtle.left(angle)
        turtle.forward(1)
        hilbert(level - 1, -angle)
        turtle.right(angle)

# draw hilbert curve
hilbert(levels)
turtle.update()
