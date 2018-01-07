def DrawRectangle(width,height):
    print("*"*width)
    for i in range(height-2):
        print("*"+" "*(width-2)+"*")
    print("*"*width)
