"""Echo - a survival game made with Python turtle.

Every 10 seconds a ghost appears and replays EXACTLY what you did during
that round. Ghosts repeat their moves every round, forever, so the longer
you survive, the more of your past selves you have to dodge.

  * Touch a ghost and it's game over.
  * Ghosts are harmless (dim) for the first second of each round.
  * The faint line in front of each ghost shows where it's about to go.
  * Grab the yellow orbs for points.

Controls: Arrow keys or WASD to move, Space to restart.
Run it with:  python echo.py
"""

import math
import random
import turtle

# ---- Settings ---------------------------------------------------------------
ARENA = 280                      # half-width of the square arena
TICK_MS = 30                     # time between frames (about 33 fps)
ROUND_SECONDS = 10
ROUND_TICKS = ROUND_SECONDS * 1000 // TICK_MS
GRACE_TICKS = 1000 // TICK_MS    # ghosts can't hurt you for the first second
PREVIEW_TICKS = 25               # how far ahead the ghost path preview goes
SPEED = 5                        # pixels per frame
HIT_DIST = 16                    # how close a ghost must be to catch you
ORB_DIST = 18                    # how close you must be to grab an orb
ORB_POINTS = 10
ROUND_POINTS = 25

BG = "#0d0f1a"
BORDER_COLOR = "#2a3050"
PLAYER_COLOR = "#4fd1ff"
DEAD_COLOR = "#ff3b3b"
ORB_COLOR = "#ffe066"
GHOST_COLORS = ["#ff5c8a", "#ffb84f", "#b48cff", "#6dff9a", "#ff7a5c", "#5cffe1"]

KEYS = {
    "Up": (0, 1), "w": (0, 1),
    "Down": (0, -1), "s": (0, -1),
    "Left": (-1, 0), "a": (-1, 0),
    "Right": (1, 0), "d": (1, 0),
}


def blend(color_a, color_b, amount):
    """Mix two '#rrggbb' colors. amount=0 gives color_a, 1 gives color_b."""
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(x + (y - x) * amount) for x, y in zip(a, b)]
    return "#%02x%02x%02x" % tuple(mixed)


def make_pen(color="white"):
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.color(color)
    return pen


class Echo:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(700, 720)
        self.screen.title("Echo")
        self.screen.bgcolor(BG)
        self.screen.tracer(0)

        self.border_pen = make_pen(BORDER_COLOR)
        self.preview_pen = make_pen()
        self.hud_pen = make_pen()
        self.msg_pen = make_pen()
        self.draw_border()

        self.player = turtle.Turtle("turtle")
        self.player.penup()
        self.player.shapesize(1.1)

        self.orb = turtle.Turtle("circle")
        self.orb.penup()
        self.orb.color(ORB_COLOR)
        self.orb.shapesize(0.6)

        self.ghosts = []     # turtle objects, one per recording
        self.held = set()    # keys currently held down
        self.key_tokens = {key: 0 for key in KEYS}
        self.msg_token = 0
        self.best = 0

        self.bind_keys()
        self.reset()
        self.tick()

    # ---- Setup --------------------------------------------------------------
    def draw_border(self):
        pen = self.border_pen
        pen.pensize(3)
        pen.goto(-ARENA, -ARENA)
        pen.pendown()
        for x, y in [(ARENA, -ARENA), (ARENA, ARENA), (-ARENA, ARENA), (-ARENA, -ARENA)]:
            pen.goto(x, y)
        pen.penup()

    def bind_keys(self):
        for key in KEYS:
            self.screen.onkeypress(lambda k=key: self.key_down(k), key)
            self.screen.onkeyrelease(lambda k=key: self.key_up(k), key)
        self.screen.onkey(self.restart, "space")
        self.screen.listen()

    def key_down(self, key):
        self.key_tokens[key] += 1
        self.held.add(key)

    def key_up(self, key):
        # Holding a key on some systems sends release+press pairs over and
        # over. Waiting a moment before letting go stops the turtle stuttering.
        token = self.key_tokens[key]

        def release():
            if self.key_tokens[key] == token:
                self.held.discard(key)

        self.screen.ontimer(release, 40)

    def reset(self):
        self.recordings = []   # one list of (x, y, heading) per finished round
        self.current = []      # what the player is doing this round
        self.round = 1
        self.t = 0             # frame number inside the current round
        self.score = 0
        self.alive = True

        self.px, self.py, self.heading = 0.0, 0.0, 90.0
        self.player.color(PLAYER_COLOR)
        self.player.goto(self.px, self.py)
        self.player.setheading(self.heading)
        self.player.showturtle()

        for ghost in self.ghosts:
            ghost.hideturtle()
        self.preview_pen.clear()
        self.msg_pen.clear()
        self.place_orb()
        self.flash_message("Move! In 10 seconds, your echo will follow you.", PLAYER_COLOR)

    def restart(self):
        if not self.alive:
            self.reset()

    # ---- Game loop ----------------------------------------------------------
    def tick(self):
        if self.alive:
            self.step()
        self.screen.update()
        self.screen.ontimer(self.tick, TICK_MS)

    def step(self):
        self.move_player()
        self.current.append((self.px, self.py, self.heading))

        if self.move_ghosts():
            self.game_over()
            return

        ox, oy = self.orb_pos
        if math.hypot(self.px - ox, self.py - oy) < ORB_DIST:
            self.score += ORB_POINTS
            self.place_orb()

        self.t += 1
        if self.t >= ROUND_TICKS:
            self.end_round()
        self.draw_hud()

    def move_player(self):
        dx = sum(KEYS[k][0] for k in self.held)
        dy = sum(KEYS[k][1] for k in self.held)
        if dx == 0 and dy == 0:
            return
        length = math.hypot(dx, dy)
        limit = ARENA - 10
        self.px = max(-limit, min(limit, self.px + dx / length * SPEED))
        self.py = max(-limit, min(limit, self.py + dy / length * SPEED))
        self.heading = math.degrees(math.atan2(dy, dx))
        self.player.goto(self.px, self.py)
        self.player.setheading(self.heading)

    def move_ghosts(self):
        """Move every ghost to its recorded spot. Returns True if one caught you."""
        self.preview_pen.clear()
        harmless = self.t < GRACE_TICKS
        caught = False

        for i, path in enumerate(self.recordings):
            ghost = self.ghosts[i]
            color = GHOST_COLORS[i % len(GHOST_COLORS)]
            gx, gy, gh = path[min(self.t, len(path) - 1)]
            ghost.goto(gx, gy)
            ghost.setheading(gh)
            ghost.color(blend(BG, color, 0.3 if harmless else 1.0))

            # Faint line showing where this ghost is headed next.
            self.preview_pen.pencolor(blend(BG, color, 0.35))
            self.preview_pen.goto(gx, gy)
            self.preview_pen.pendown()
            end = min(self.t + PREVIEW_TICKS, len(path) - 1)
            for x, y, _ in path[self.t + 1:end + 1:3]:
                self.preview_pen.goto(x, y)
            self.preview_pen.penup()

            if not harmless and math.hypot(self.px - gx, self.py - gy) < HIT_DIST:
                caught = True

        return caught

    def end_round(self):
        self.recordings.append(self.current)
        self.current = []
        self.t = 0
        self.round += 1
        self.score += ROUND_POINTS

        if len(self.ghosts) < len(self.recordings):
            ghost = turtle.Turtle("turtle")
            ghost.penup()
            ghost.shapesize(1.1)
            self.ghosts.append(ghost)
        number = len(self.recordings)
        self.ghosts[number - 1].showturtle()

        color = GHOST_COLORS[(number - 1) % len(GHOST_COLORS)]
        self.flash_message(f"Echo #{number} awakens...", color)

    def game_over(self):
        self.alive = False
        self.best = max(self.best, self.score)
        self.player.color(DEAD_COLOR)
        self.preview_pen.clear()
        self.draw_hud()

        self.msg_token += 1
        pen = self.msg_pen
        pen.clear()
        pen.color(DEAD_COLOR)
        pen.goto(0, 40)
        pen.write("CAUGHT BY YOUR PAST", align="center", font=("Arial", 28, "bold"))
        pen.color("white")
        pen.goto(0, 0)
        survived = self.round - 1
        rounds = "round" if survived == 1 else "rounds"
        pen.write(f"Score: {self.score}    Survived {survived} {rounds}    Best: {self.best}",
                  align="center", font=("Arial", 16, "normal"))
        pen.goto(0, -35)
        pen.write("Press Space to play again", align="center", font=("Arial", 14, "normal"))

    # ---- Helpers ------------------------------------------------------------
    def place_orb(self):
        limit = ARENA - 30
        for _ in range(100):
            x = random.uniform(-limit, limit)
            y = random.uniform(-limit, limit)
            if math.hypot(x - self.px, y - self.py) > 120:
                break
        self.orb_pos = (x, y)
        self.orb.goto(x, y)

    def draw_hud(self):
        pen = self.hud_pen
        pen.clear()
        pen.color("white")
        pen.goto(-ARENA, ARENA + 15)
        pen.write(f"Round {self.round}", font=("Arial", 14, "bold"))
        pen.goto(0, ARENA + 15)
        pen.write(f"Echoes: {len(self.recordings)}", align="center", font=("Arial", 14, "normal"))
        pen.goto(ARENA, ARENA + 15)
        pen.write(f"Score: {self.score}", align="right", font=("Arial", 14, "bold"))

        # Bar under the arena showing time left until the next echo.
        progress = self.t / ROUND_TICKS
        pen.pensize(6)
        pen.goto(-ARENA, -ARENA - 20)
        pen.pencolor(BORDER_COLOR)
        pen.pendown()
        pen.goto(ARENA, -ARENA - 20)
        pen.penup()
        pen.goto(-ARENA, -ARENA - 20)
        pen.pencolor(blend(PLAYER_COLOR, DEAD_COLOR, progress))
        pen.pendown()
        pen.goto(-ARENA + 2 * ARENA * progress, -ARENA - 20)
        pen.penup()

    def flash_message(self, text, color):
        self.msg_token += 1
        token = self.msg_token
        pen = self.msg_pen
        pen.clear()
        pen.color(color)
        pen.goto(0, -ARENA - 55)
        pen.write(text, align="center", font=("Arial", 14, "italic"))

        def hide():
            if self.msg_token == token:
                pen.clear()

        self.screen.ontimer(hide, 2000)


if __name__ == "__main__":
    Echo()
    turtle.mainloop()
