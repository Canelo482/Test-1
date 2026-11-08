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

colors = ["red" , "orange", "yellow" , "green", "blue", "purple", "pink", "black","brown", "grey"]

painter.color(random.choice(colors))

painter.goto(random.randint(-327,327), random.randint(-250,213))

def teleportation(x,y):
    painter. stamp()
    painter.color(random.choice(colors))
    painter.hideturtle()
    painter.goto(random.randint(-327,327), random.randint(-250,213))
    painter.showturtle()

painter.onclick(teleportation)



wn = turtle.Screen()
wn.mainloop()
