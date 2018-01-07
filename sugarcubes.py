comments = []
comments.append("Nice meeting you!")
comments.append("Would love to know you better")
comments.append("You are a nice person")
comments.append("Keep smiling")
comments.append("Hope you had a great semester :)")
comments.append("Enjoy your vacations")
comments.append("Screw GPA. Enjoy life")
comments.append("Stress doesn't suit you. Chillax!")
#append as many comments as possible

import random

commentsfile = open("comments.html","w")
commentsfile.write("<html>")
namesfile = open("nameslist.txt","r")
for name in namesfile.readlines():
    thecomment = random.choice(comments)
    thehtml = "<div style='color: cadetblue;font-family:verdana'>"+name.capitalize()+"<br>"+thecomment+"<br>M.Hamza Ali</div><br>"
    commentsfile.write(thehtml)
    
commentsfile.write("</html>")

commentsfile.close()
