"""Turtle Runner - an endless running game made with Python turtle.

Your turtle runs along the beach. Jump over rocks, duck under seagulls,
and see how far you can get. The game keeps getting faster, and day
turns to night every 500 points.

Controls:
  Space / Up / W  - jump (press again in the air to double jump)
  Down / S        - duck (in the air, it makes you drop faster)
  Space           - start / play again
Run it with:  python turtle_runner.py
"""

import random
import time

import turtle

# ---- Settings ---------------------------------------------------------------
WIDTH, HEIGHT = 800, 400
GROUND_Y = -110            # where the turtle's feet touch the ground
PLAYER_X = -280
TICK_MS = 20               # 50 frames per second

GRAVITY = 0.6
JUMP_SPEED = 11
DOUBLE_JUMP_SPEED = 9
FAST_FALL = 3              # gravity multiplier when ducking in the air

START_SPEED = 6            # pixels per frame
MAX_SPEED = 14
SPEED_UP = 0.0025          # added to the speed every frame
BIRD_SCORE = 250           # seagulls start showing up after this score
NIGHT_EVERY = 500          # day/night switches every this many points

DAY = {"bg": "#cfeeff", "ground": "#c9a66b", "line": "#8a6b45",
       "text": "#22313f", "cloud": "#ffffff", "pebble": "#8a6b45"}
NIGHT = {"bg": "#18213d", "ground": "#4d4030", "line": "#7a6548",
         "text": "#e8ecff", "cloud": "#3a4670", "pebble": "#7a6548"}
PLAYER_COLOR = "#2e9e4f"
ROCK_COLOR = "#7d7d86"
BIRD_COLOR = "#5a5f70"

# How the player looks and its hitbox when standing or ducking.
#   size = turtle shapesize, lift = how high its centre sits above its feet,
#   hw/hh = half width/height of the hitbox, dx = hitbox offset forwards.
STAND = {"size": (1.4, 1.4), "lift": 12.6, "hw": 14, "hh": 11, "dx": 5}
DUCK = {"size": (0.8, 1.7), "lift": 7.2, "hw": 17, "hh": 6, "dx": 7}

# Obstacles: (shape name, width, height)
ROCKS = [("rock_small", 22, 20), ("rock_big", 30, 32), ("rock_double", 52, 24)]
BIRD_SIZE = (30, 14)
BIRD_HEIGHTS = [14, 25]    # height of the bird's centre above the ground:
                           # 14 = you must jump, 25 = duck (or jump high)


# ---- Shapes -----------------------------------------------------------------
# These are drawn with heading 90, so x is left/right and y is up/down.
def rock_shape(w, h, lumps):
    if lumps == 1:
        return ((-w / 2, -h / 2), (-w / 2, h * 0.1), (-w * 0.3, h / 2),
                (w * 0.1, h * 0.45), (w * 0.4, h * 0.2), (w / 2, -h / 2))
    return ((-w / 2, -h / 2), (-w / 2, 0), (-w * 0.3, h / 2), (-w * 0.1, h * 0.1),
            (w * 0.1, h * 0.35), (w * 0.35, h / 2), (w / 2, 0), (w / 2, -h / 2))


BIRD_UP = ((-15, 7), (-7, -1), (0, -3), (7, -1), (15, 7), (7, -5), (0, -7), (-7, -5))
BIRD_DOWN = ((-15, -7), (-7, 1), (0, 3), (7, 1), (15, -7), (7, -3), (0, -1), (-7, -3))


def make_pen():
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    return pen


# ---- The game ---------------------------------------------------------------
class TurtleRunner:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.title("Turtle Runner")
        self.screen.tracer(0)
        for name, w, h in ROCKS:
            self.screen.register_shape(name, rock_shape(w, h, 2 if "double" in name else 1))
        self.screen.register_shape("bird_up", BIRD_UP)
        self.screen.register_shape("bird_down", BIRD_DOWN)

        self.ground_pen = make_pen()
        self.hud_pen = make_pen()
        self.msg_pen = make_pen()

        self.clouds = []
        for i in range(3):
            cloud = turtle.Turtle("circle")
            cloud.penup()
            cloud.shapesize(1.2, 3)
            cloud.goto(-250 + i * 300, random.randint(40, 150))
            self.clouds.append(cloud)

        self.pebbles = []
        for _ in range(14):
            pebble = turtle.Turtle("square")
            pebble.penup()
            pebble.shapesize(0.15, 0.35)
            pebble.goto(random.uniform(-WIDTH / 2, WIDTH / 2),
                        GROUND_Y - random.uniform(6, 60))
            self.pebbles.append(pebble)

        self.player = turtle.Turtle("turtle")
        self.player.penup()
        self.player.color(PLAYER_COLOR)

        self.obstacles = []   # each one is a dict with its turtle and hitbox
        self.pool = []        # spare obstacle turtles to reuse
        self.held = set()
        self.key_tokens = {}
        self.best = 0
        self.ended_at = 0.0

        for key in ("space", "Up", "w"):
            self.bind_key(key, self.jump)
        for key in ("Down", "s"):
            self.bind_key(key, lambda: None)
        self.screen.listen()

        self.reset()
        self.state = "ready"
        self.show_title()
        self.tick()

    # ---- Keys ---------------------------------------------------------------
    def bind_key(self, key, on_press):
        # Holding a key on some systems sends release+press pairs over and
        # over. Waiting a moment before treating it as released means holding
        # jump won't keep jumping, and holding duck stays smooth.
        def press():
            self.key_tokens[key] = self.key_tokens.get(key, 0) + 1
            if key not in self.held:
                self.held.add(key)
                on_press()

        def release():
            token = self.key_tokens.get(key, 0)

            def let_go():
                if self.key_tokens.get(key, 0) == token:
                    self.held.discard(key)

            self.screen.ontimer(let_go, 40)

        self.screen.onkeypress(press, key)
        self.screen.onkeyrelease(release, key)

    # ---- Setup --------------------------------------------------------------
    def reset(self):
        for ob in self.obstacles:
            ob["turtle"].hideturtle()
            self.pool.append(ob["turtle"])
        self.obstacles = []
        self.y = 0.0            # height of the turtle's feet above the ground
        self.vy = 0.0
        self.jumps_used = 0
        self.ducking = False
        self.speed = START_SPEED
        self.distance = 0.0
        self.score = 0
        self.frame = 0
        self.next_gap = 400
        self.night = False
        self.apply_theme()
        self.update_player()
        self.draw_hud()

    def start(self):
        self.reset()
        self.msg_pen.clear()
        self.state = "playing"

    def apply_theme(self):
        theme = NIGHT if self.night else DAY
        self.theme = theme
        self.screen.bgcolor(theme["bg"])
        for cloud in self.clouds:
            cloud.color(theme["cloud"])
        for pebble in self.pebbles:
            pebble.color(theme["pebble"])

        pen = self.ground_pen
        pen.clear()
        pen.goto(-WIDTH / 2, GROUND_Y)
        pen.color(theme["ground"])
        pen.begin_fill()
        for x, y in [(WIDTH / 2, GROUND_Y), (WIDTH / 2, -HEIGHT / 2),
                     (-WIDTH / 2, -HEIGHT / 2), (-WIDTH / 2, GROUND_Y)]:
            pen.goto(x, y)
        pen.end_fill()
        pen.pencolor(theme["line"])
        pen.pensize(3)
        pen.pendown()
        pen.goto(WIDTH / 2, GROUND_Y)
        pen.penup()

    # ---- Actions ------------------------------------------------------------
    def jump(self):
        if self.state != "playing":
            # Short pause after crashing so a held jump doesn't restart instantly.
            if time.time() - self.ended_at > 0.5:
                self.start()
            return
        if self.y == 0 and self.vy == 0:
            self.vy = JUMP_SPEED
            self.jumps_used = 1
        elif self.jumps_used < 2:
            self.vy = DOUBLE_JUMP_SPEED
            self.jumps_used = 2

    def spawn(self):
        t = self.pool.pop() if self.pool else turtle.Turtle()
        t.penup()
        t.setheading(90)
        if self.score >= BIRD_SCORE and random.random() < 0.3:
            w, h = BIRD_SIZE
            height = random.choice(BIRD_HEIGHTS)
            t.shape("bird_up")
            t.color(BIRD_COLOR)
            ob = {"kind": "bird", "w": w, "h": h, "y": GROUND_Y + height, "extra": 1}
        else:
            name, w, h = random.choice(ROCKS)
            t.shape(name)
            t.color(ROCK_COLOR)
            ob = {"kind": "rock", "w": w, "h": h, "y": GROUND_Y + h / 2, "extra": 0}
        ob["turtle"] = t
        ob["x"] = WIDTH / 2 + 40
        t.goto(ob["x"], ob["y"])
        t.showturtle()
        self.obstacles.append(ob)

    # ---- Game loop ----------------------------------------------------------
    def tick(self):
        if self.state == "playing":
            self.update()
        self.screen.update()
        self.screen.ontimer(self.tick, TICK_MS)

    def update(self):
        self.frame += 1
        self.speed = min(MAX_SPEED, self.speed + SPEED_UP)
        self.distance += self.speed
        self.score = int(self.distance / 10)

        night = (self.score // NIGHT_EVERY) % 2 == 1
        if night != self.night:
            self.night = night
            self.apply_theme()

        # Jumping and falling.
        self.ducking = "Down" in self.held or "s" in self.held
        if self.y > 0 or self.vy != 0:
            self.vy -= GRAVITY * (FAST_FALL if self.ducking else 1)
            self.y += self.vy
            if self.y <= 0:
                self.y, self.vy, self.jumps_used = 0.0, 0.0, 0
        self.update_player()

        # Scenery.
        for cloud in self.clouds:
            x = cloud.xcor() - self.speed * 0.2
            cloud.goto(x if x > -WIDTH / 2 - 60 else WIDTH / 2 + 60, cloud.ycor())
        for pebble in self.pebbles:
            x = pebble.xcor() - self.speed
            pebble.goto(x if x > -WIDTH / 2 - 5 else WIDTH / 2 + 5, pebble.ycor())

        # New obstacles. The gap grows with speed so jumps stay possible.
        self.next_gap -= self.speed
        if self.next_gap <= 0:
            self.spawn()
            self.next_gap = random.uniform(self.speed * 40, self.speed * 75)

        # Move obstacles and check for crashes.
        body = self.posture()
        px = PLAYER_X + body["dx"]
        py = GROUND_Y + self.y + body["lift"]
        for ob in list(self.obstacles):
            ob["x"] -= self.speed + ob["extra"]
            t = ob["turtle"]
            t.goto(ob["x"], ob["y"])
            if ob["kind"] == "bird" and self.frame % 8 == 0:
                t.shape("bird_down" if t.shape() == "bird_up" else "bird_up")

            if ob["x"] < -WIDTH / 2 - 60:
                t.hideturtle()
                self.obstacles.remove(ob)
                self.pool.append(t)
            elif (abs(px - ob["x"]) < body["hw"] + ob["w"] / 2 - 2 and
                  abs(py - ob["y"]) < body["hh"] + ob["h"] / 2 - 2):
                self.game_over()
                return

        self.draw_hud()

    def posture(self):
        return DUCK if self.ducking and self.y == 0 else STAND

    def update_player(self):
        body = self.posture()
        self.player.shapesize(*body["size"])
        self.player.goto(PLAYER_X, GROUND_Y + self.y + body["lift"])

    # ---- Text ---------------------------------------------------------------
    def draw_hud(self):
        pen = self.hud_pen
        pen.clear()
        pen.color(self.theme["text"])
        pen.goto(WIDTH / 2 - 20, HEIGHT / 2 - 40)
        pen.write(f"Best {self.best:05d}    Score {self.score:05d}", align="right",
                  font=("Courier", 16, "bold"))

    def write_box(self, lines):
        pen = self.msg_pen
        pen.clear()
        pen.color(self.theme["text"])
        y = 60
        for text, size, style in lines:
            pen.goto(0, y)
            pen.write(text, align="center", font=("Arial", size, style))
            y -= size + 16

    def show_title(self):
        self.write_box([
            ("TURTLE RUNNER", 28, "bold"),
            ("Space / Up: jump (press again in the air to double jump)", 13, "normal"),
            ("Down: duck under seagulls", 13, "normal"),
            ("Press Space to start", 14, "italic"),
        ])

    def game_over(self):
        self.state = "over"
        self.ended_at = time.time()
        new_best = self.score > self.best
        self.best = max(self.best, self.score)
        self.player.color("#d64545")
        self.draw_hud()
        self.write_box([
            ("GAME OVER", 28, "bold"),
            (f"Score: {self.score}" + ("   NEW BEST!" if new_best else ""), 16, "bold"),
            ("Press Space to run again", 14, "italic"),
        ])
        self.screen.ontimer(lambda: self.player.color(PLAYER_COLOR), 600)


if __name__ == "__main__":
    TurtleRunner()
    turtle.mainloop()
