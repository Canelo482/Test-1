import random
import turtle

GROUND_Y = -100
PLAYER_Y = -87
GRAVITY = 0.8
JUMP_POWER = 13

screen = turtle.Screen()
screen.setup(800, 400)
screen.title("Turtle Runner")
screen.bgcolor("lightblue")
screen.tracer(0)

ground = turtle.Turtle(visible=False)
ground.penup()
ground.goto(-400, GROUND_Y)
ground.pendown()
ground.pensize(3)
ground.goto(400, GROUND_Y)

player = turtle.Turtle("turtle")
player.color("green")
player.shapesize(1.5)
player.penup()
player.goto(-300, PLAYER_Y)

rock = turtle.Turtle("square")
rock.color("gray")
rock.shapesize(1.5, 1)
rock.penup()
rock.goto(450, GROUND_Y + 15)

pen = turtle.Turtle(visible=False)
pen.penup()

velocity = 0
speed = 6
score = 0
game_over = False


def show_score():
    pen.clear()
    pen.goto(0, 150)
    pen.write("Score: " + str(score), align="center", font=("Arial", 18, "bold"))


def jump():
    global velocity
    if game_over:
        restart()
    elif player.ycor() == PLAYER_Y:
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
        velocity -= GRAVITY
        y = player.ycor() + velocity
        if y <= PLAYER_Y:
            y = PLAYER_Y
            velocity = 0
        player.sety(y)

        rock.setx(rock.xcor() - speed)
        if rock.xcor() < -420:
            rock.setx(random.randint(420, 700))
            score += 1
            speed = min(speed + 0.3, 15)
            show_score()

        if player.distance(rock) < 25:
            game_over = True
            pen.goto(0, 0)
            pen.write("GAME OVER - press Space", align="center", font=("Arial", 24, "bold"))

    screen.update()
    screen.ontimer(game_loop, 20)


screen.onkeypress(jump, "space")
screen.listen()
show_score()
game_loop()
turtle.mainloop()
