# turtle clicking game
# click the turtle and it moves somewhere else!!

import turtle
import random

wn = turtle.Screen()
wn.title("turtle clicking game")
wn.setup(800,600)
wn.bgcolor("white")

score = 0

# list of colors the turtle can be
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "cyan", "magenta"]

# make the turtle
t = turtle.Turtle()
t.shape("turtle")
t.shapesize(2,2)
t.penup()
t.speed(0)

# random color from the list
t.color(random.choice(colors))

t.goto(random.randint(-350,350), random.randint(-250,220))

# this turtle writes the score
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.goto(0,260)
pen.write("Score: 0", align="center", font=("Arial", 16, "normal"))


def clicked(x,y):
    global score
    #print(x,y)
    t.stamp() # leaves a mark
    score = score + 1
    pen.clear()
    pen.write("Score: " + str(score), align="center", font=("Arial", 16, "normal"))

    # new color
    t.color(random.choice(colors))
    t.setheading(random.randint(0,360))

    # teleport!
    t.hideturtle()
    t.goto(random.randint(-350,350),random.randint(-250,220))
    t.showturtle()


t.onclick(clicked)

turtle.done()
