"""Turtle Clicking Game.

A turtle-shaped turtle with a random color appears somewhere on the screen.
Click it and it leaves a stamped mark of itself where it was, then teleports
to a new random spot with a new random color and heading.

Controls:
    Left-click the turtle  -> stamp + teleport (+1 point)
    C                      -> clear all marks and reset the score
    Q / Escape             -> quit

Run with:  python turtle_click_game.py
"""

import random
import turtle

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TURTLE_SIZE = 2          # stretch factor for the turtle shape (1 = default 20px)
EDGE_MARGIN = 40         # keep the turtle this far from the window edges
HUD_HEIGHT = 50          # space reserved at the top for the score text


def random_color():
    """Return a random, reasonably bright RGB color (0-1 floats)."""
    return (random.uniform(0.1, 1), random.uniform(0.1, 1), random.uniform(0.1, 1))


def random_position(screen):
    """Return a random (x, y) inside the current window, away from the edges."""
    half_w = screen.window_width() // 2 - EDGE_MARGIN
    half_h = screen.window_height() // 2 - EDGE_MARGIN
    x = random.randint(-half_w, half_w)
    y = random.randint(-half_h, half_h - HUD_HEIGHT)
    return x, y


class TurtleClickGame:
    def __init__(self):
        self.score = 0

        self.screen = turtle.Screen()
        self.screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen.title("Turtle Clicking Game")
        self.screen.bgcolor("white")
        self.screen.colormode(1.0)

        # The turtle the player clicks on.
        self.player = turtle.Turtle(shape="turtle")
        self.player.shapesize(TURTLE_SIZE, TURTLE_SIZE, 2)
        self.player.penup()
        self.player.speed(0)  # instant moves = a "teleport" with no animation

        # Invisible turtle used only to draw the score.
        self.hud = turtle.Turtle(visible=False)
        self.hud.penup()
        self.hud.speed(0)

        self.player.onclick(self.on_turtle_click)
        self.screen.onkey(self.clear_marks, "c")
        self.screen.onkey(self.clear_marks, "C")
        self.screen.onkey(self.screen.bye, "q")
        self.screen.onkey(self.screen.bye, "Escape")
        self.screen.listen()

        self.teleport()
        self.draw_score()

    def teleport(self):
        """Move the turtle to a random spot with a new color and heading."""
        self.player.hideturtle()
        self.player.color(random_color())
        self.player.setheading(random.randint(0, 359))
        self.player.goto(random_position(self.screen))
        self.player.showturtle()

    def on_turtle_click(self, x, y):
        # Ignore extra clicks while this one is being handled.
        self.player.onclick(None)

        self.player.stamp()   # leave a mark of the turtle where it was
        self.score += 1
        self.draw_score()
        self.teleport()

        self.player.onclick(self.on_turtle_click)

    def clear_marks(self):
        """Remove all stamped marks and reset the score."""
        self.player.clearstamps()
        self.score = 0
        self.draw_score()

    def draw_score(self):
        self.hud.clear()
        self.hud.goto(0, self.screen.window_height() // 2 - 40)
        self.hud.write(
            f"Score: {self.score}    (C = clear, Q = quit)",
            align="center",
            font=("Arial", 16, "bold"),
        )

    def run(self):
        self.screen.mainloop()


if __name__ == "__main__":
    TurtleClickGame().run()
