"""Turtle Runner (simple version).

Press Space to jump over the rocks. Each rock you pass is 1 point,
and the game gets a little faster every time.
Run it with:  python turtle_runner.py
"""

import random
import turtle

GROUND_Y = -100     # height of the ground line
PLAYER_Y = -87      # turtle's height when standing on the ground
GRAVITY = 0.8       # how fast the turtle falls
JUMP_POWER = 13     # how high the turtle jumps

# ---- Background ----
screen = turtle.Screen()
screen.setup(800, 400)
screen.title("Turtle Runner")
screen.bgcolor("lightblue")
screen.tracer(0)    # draw everything at once, so it doesn't flicker

# ---- Ground ----
ground = turtle.Turtle(visible=False)
ground.penup()
ground.goto(-400, GROUND_Y)
ground.pendown()
ground.pensize(3)
ground.goto(400, GROUND_Y)

# ---- Player ----
player = turtle.Turtle("turtle")
player.color("green")
player.shapesize(1.5)
player.penup()
player.goto(-300, PLAYER_Y)

# ---- Obstacle ----
rock = turtle.Turtle("square")
rock.color("gray")
rock.shapesize(1.5, 1)      # 30 pixels tall, 20 wide
rock.penup()
rock.goto(450, GROUND_Y + 15)

# ---- Score ----
pen = turtle.Turtle(visible=False)
pen.penup()

velocity = 0        # how fast the turtle is moving up (+) or down (-)
speed = 6           # how fast the rock moves left
score = 0
game_over = False


def show_score():
    pen.clear()
    pen.goto(0, 150)
    pen.write(f"Score: {score}", align="center", font=("Arial", 18, "bold"))


def jump():
    global velocity
    if game_over:
        restart()
    elif player.ycor() == PLAYER_Y:     # can only jump from the ground
        velocity = JUMP_POWER


def restart():
    global velocity, speed, score, game_over
    velocity = 0
    speed = 6
    score = 0
    game_over = False
    player.sety(PLAYER_Y)
    rock.setx(450)
    show_score()


def game_loop():
    global velocity, speed, score, game_over
    if not game_over:
        # Gravity pulls the turtle down; the ground stops it.
        velocity -= GRAVITY
        y = player.ycor() + velocity
        if y <= PLAYER_Y:
            y = PLAYER_Y
            velocity = 0
        player.sety(y)

        # Move the rock left. When it leaves the screen, send it back.
        rock.setx(rock.xcor() - speed)
        if rock.xcor() < -420:
            rock.setx(random.randint(420, 700))
            score += 1
            speed = min(speed + 0.3, 15)    # gets faster, up to 15
            show_score()

        # Crash!
        if player.distance(rock) < 25:
            game_over = True
            pen.goto(0, 0)
            pen.write("GAME OVER - press Space", align="center", font=("Arial", 24, "bold"))

    screen.update()
    screen.ontimer(game_loop, 20)    # run again in 20 ms


screen.onkeypress(jump, "space")
screen.listen()
show_score()
game_loop()
turtle.mainloop()
