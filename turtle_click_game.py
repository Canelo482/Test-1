import turtle
import random

painter = turtle.Turtle()
pop_up = turtle.Screen()
pop_up.title("Turtle Game")


score = 0

painter.shape("turtle")
painter.turtlesize(2,2)
painter.penup()
painter.speed(0)

# r1 = random.randint(0.)
# r2 = random.randint(0.)
# r3 = random.randint(0.)

colors = ["red" , "orange", "yellow" , "green", "blue", "purple", "pink", "brown", "grey"]

painter.color("black")

painter.goto(random.randint(-300,300), random.randint(-250,213))

def teleportation(x,y):
    painter.color(random.choice(colors))
    painter. stamp()
    painter.color("black")
    size = random.randint(1,4)
    painter.turtlesize(size,size)
    painter.hideturtle()
    painter.penup()
    painter.goto(random.randint(-300,300), random.randint(-250,213))
    painter.pendown()
    painter.showturtle()

painter.onclick(teleportation)



wn = turtle.Screen()
wn.mainloop()
