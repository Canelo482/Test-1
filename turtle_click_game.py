import turtle
import random

painter = turtle.Turtle()
pop_up = turtle.Screen()
pop_up. title ("Turtle Game")


score = 0

painter.shape("turtle")
painter.turtlesize(2,2)
painter.penup()
painter.speed(0)


colors = ["red" , "orange", "yellow" , "green", "blue", "purple", "pink", "brown", "grey"]

painter.color(random.choice(colors))

painter.goto(random.randint(-327,327), random.randint(-250,213))

painter.color("black")

# scoreboard in the top right corner
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(pop_up.window_width()/2 - 30, pop_up.window_height()/2 - 60)
scoreboard.write(score, align="right", font=("Arial", 30, "bold"))

# countdown timer in the top left corner
time_left = 24
timer = turtle.Turtle()
timer.hideturtle()
timer.penup()
timer.goto(-pop_up.window_width()/2 + 30, pop_up.window_height()/2 - 60)
timer.write(time_left, align="left", font=("Arial", 30, "bold"))

def countdown():
    global time_left
    time_left = time_left - 1
    timer.clear()
    timer.write(time_left, align="left", font=("Arial", 30, "bold"))
    if time_left > 0:
        pop_up.ontimer(countdown, 1000)  # run again in 1 second
    else:
        painter.onclick(None)  # times up, turtle cant be clicked anymore

pop_up.ontimer(countdown, 1000)


def teleportation(x,y):
    global score
    painter.color(random.choice(colors))
    painter. stamp()
    painter.color("black")
    score = score + 1
    scoreboard.clear()
    scoreboard.write(score, align="right", font=("Arial", 30, "bold"))
    size_of_turtle = random.randint(1,4)
    painter.turtlesize(size_of_turtle , size_of_turtle)
    painter.penup()
    painter.goto(random.randint(-280,280), random.randint(-250,213))
    painter.pendown()

painter.onclick(teleportation)


wn = turtle.Screen()
wn.mainloop()
