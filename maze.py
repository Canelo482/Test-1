"""Star Maze - a maze game made with Python turtle.

Guide your turtle through the maze and collect all 3 stars before the
1 minute timer runs out. Watch out for the monster: it wanders the maze,
and if it spots you nearby it will chase you. If it touches you, the
mission fails.

Controls: Arrow keys or WASD to move, Space to start a new maze.
Run it with:  python maze.py
"""

import math
import random
import time
from collections import deque

import turtle

# ---- Settings ---------------------------------------------------------------
MAZE_COLS = 14          # maze size in "rooms" (the grid of tiles is 2x+1)
MAZE_ROWS = 10
TILE = 26               # size of one tile in pixels
TIME_LIMIT = 60         # seconds
STARS_NEEDED = 3
MONSTER_STEP = 0.33     # seconds between monster moves (smaller = faster)
CHASE_RANGE = 12        # monster chases you when this many steps away or closer
MOVE_COOLDOWN = 0.09    # stops the turtle zooming when a key is held down
TICK_MS = 50

BG = "#10131f"
WALL_COLOR = "#3b4a7a"
FLOOR_COLOR = "#161a2b"
PLAYER_COLOR = "#5cff8f"
MONSTER_COLOR = "#ff4b5c"
STAR_COLOR = "#ffd84f"
TEXT_COLOR = "white"

MOVES = {
    "Up": (0, -1), "w": (0, -1),
    "Down": (0, 1), "s": (0, 1),
    "Left": (-1, 0), "a": (-1, 0),
    "Right": (1, 0), "d": (1, 0),
}
HEADINGS = {(0, -1): 90, (0, 1): 270, (-1, 0): 180, (1, 0): 0}


# ---- Maze building ----------------------------------------------------------
def generate_maze(cols, rows):
    """Return a grid of booleans (True = wall) with a random maze carved in it."""
    width, height = 2 * cols + 1, 2 * rows + 1
    grid = [[True] * width for _ in range(height)]

    # Carve a "perfect" maze with a depth-first search.
    start = (0, 0)
    grid[1][1] = False
    visited = {start}
    stack = [start]
    while stack:
        cx, cy = stack[-1]
        options = []
        for dx, dy in HEADINGS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                options.append((nx, ny))
        if not options:
            stack.pop()
            continue
        nx, ny = random.choice(options)
        grid[cy + ny + 1][cx + nx + 1] = False      # knock down the wall between
        grid[2 * ny + 1][2 * nx + 1] = False        # open the new room
        visited.add((nx, ny))
        stack.append((nx, ny))

    # Knock out some extra walls so there are loops to escape the monster.
    removed = 0
    while removed < cols * rows // 6:
        x = random.randrange(1, width - 1)
        y = random.randrange(1, height - 1)
        if grid[y][x] and (x + y) % 2 == 1:         # a wall sitting between two rooms
            grid[y][x] = False
            removed += 1
    return grid


def distances_from(grid, start):
    """Number of steps from start to every reachable floor tile."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in HEADINGS:
            nxt = (x + dx, y + dy)
            if nxt not in dist and not grid[nxt[1]][nxt[0]]:
                dist[nxt] = dist[(x, y)] + 1
                queue.append(nxt)
    return dist


# ---- Shapes -----------------------------------------------------------------
def star_points(spikes, outer, inner):
    points = []
    for i in range(spikes * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.pi * i / spikes
        points.append((radius * math.sin(angle), radius * math.cos(angle)))
    return tuple(points)


def make_pen(color=TEXT_COLOR):
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.color(color)
    return pen


# ---- The game ---------------------------------------------------------------
class MazeGame:
    def __init__(self):
        self.width = (2 * MAZE_COLS + 1) * TILE
        self.height = (2 * MAZE_ROWS + 1) * TILE

        self.screen = turtle.Screen()
        self.screen.setup(self.width + 60, self.height + 120)
        self.screen.title("Star Maze")
        self.screen.bgcolor(BG)
        self.screen.tracer(0)
        self.screen.register_shape("star", star_points(5, 11, 4.5))
        self.screen.register_shape("monster", star_points(9, 12, 7))

        self.wall_stamper = turtle.Turtle("square", visible=False)
        self.wall_stamper.penup()
        self.wall_stamper.color(WALL_COLOR)
        self.wall_stamper.shapesize(TILE / 20)

        self.floor_pen = make_pen(FLOOR_COLOR)
        self.hud_pen = make_pen()
        self.msg_pen = make_pen()

        self.player = turtle.Turtle("turtle")
        self.player.penup()
        self.player.color(PLAYER_COLOR)
        self.player.shapesize(0.8)

        self.monster = turtle.Turtle("monster")
        self.monster.penup()
        self.monster.color(MONSTER_COLOR)
        self.monster.shapesize(0.9)

        self.star_turtles = []
        for _ in range(STARS_NEEDED):
            star = turtle.Turtle("star")
            star.penup()
            star.color(STAR_COLOR)
            star.setheading(90)
            self.star_turtles.append(star)

        for key, step in MOVES.items():
            self.screen.onkeypress(lambda s=step: self.move_player(s), key)
        self.screen.onkey(self.new_game, "space")
        self.screen.listen()

        self.new_game()
        self.tick()

    # ---- Setup --------------------------------------------------------------
    def to_screen(self, tile):
        """Turn a (column, row) tile into turtle x, y coordinates."""
        col, row = tile
        x = -self.width / 2 + col * TILE + TILE / 2
        y = self.height / 2 - row * TILE - TILE / 2 - 30   # leave room for the HUD
        return x, y

    def new_game(self):
        self.grid = generate_maze(MAZE_COLS, MAZE_ROWS)
        self.draw_maze()

        self.player_tile = (1, 1)
        from_player = distances_from(self.grid, self.player_tile)

        # Monster starts as far from you as possible.
        self.monster_tile = max(from_player, key=from_player.get)

        # Stars go in spots away from the start and away from each other.
        self.stars = []
        spots = [t for t, d in from_player.items() if d >= 10 and t != self.monster_tile]
        random.shuffle(spots)
        for spot in spots:
            if all(abs(spot[0] - s[0]) + abs(spot[1] - s[1]) >= 8 for s in self.stars):
                self.stars.append(spot)
            if len(self.stars) == STARS_NEEDED:
                break
        for spot in spots:                       # backup if the maze was cramped
            if len(self.stars) == STARS_NEEDED:
                break
            if spot not in self.stars:
                self.stars.append(spot)

        for star, spot in zip(self.star_turtles, self.stars):
            star.goto(self.to_screen(spot))
            star.showturtle()

        self.collected = 0
        self.state = "playing"
        self.end_time = time.time() + TIME_LIMIT
        self.last_monster_move = time.time()
        self.last_player_move = 0.0

        self.player.goto(self.to_screen(self.player_tile))
        self.player.setheading(0)
        self.player.color(PLAYER_COLOR)
        self.monster.goto(self.to_screen(self.monster_tile))
        self.msg_pen.clear()
        self.draw_hud()

    def draw_maze(self):
        self.wall_stamper.clearstamps()
        self.floor_pen.clear()

        # Floor background.
        left, top = -self.width / 2, self.height / 2 - 30
        self.floor_pen.goto(left, top)
        self.floor_pen.begin_fill()
        for x, y in [(left + self.width, top), (left + self.width, top - self.height),
                     (left, top - self.height), (left, top)]:
            self.floor_pen.goto(x, y)
        self.floor_pen.end_fill()

        for row, line in enumerate(self.grid):
            for col, is_wall in enumerate(line):
                if is_wall:
                    self.wall_stamper.goto(self.to_screen((col, row)))
                    self.wall_stamper.stamp()

    # ---- Movement -----------------------------------------------------------
    def move_player(self, step):
        if self.state != "playing":
            return
        now = time.time()
        if now - self.last_player_move < MOVE_COOLDOWN:
            return
        self.player.setheading(HEADINGS[step])
        target = (self.player_tile[0] + step[0], self.player_tile[1] + step[1])
        if self.grid[target[1]][target[0]]:
            return                                # bumped into a wall
        self.last_player_move = now
        self.player_tile = target
        self.player.goto(self.to_screen(target))

        if target in self.stars:
            index = self.stars.index(target)
            self.stars[index] = None
            self.star_turtles[index].hideturtle()
            self.collected += 1
            if self.collected == STARS_NEEDED:
                self.end("won")
                return
        self.check_caught()
        self.draw_hud()

    def move_monster(self):
        from_player = distances_from(self.grid, self.player_tile)
        x, y = self.monster_tile
        neighbours = [(x + dx, y + dy) for dx, dy in HEADINGS
                      if not self.grid[y + dy][x + dx]]
        if from_player.get(self.monster_tile, 999) <= CHASE_RANGE:
            # Chase: step to the neighbour closest to the player.
            target = min(neighbours, key=lambda t: from_player.get(t, 999))
        else:
            # Wander: keep going forward, avoid turning back unless stuck.
            forward = [t for t in neighbours if t != getattr(self, "monster_prev", None)]
            target = random.choice(forward or neighbours)
        self.monster_prev = self.monster_tile
        self.monster_tile = target
        self.monster.goto(self.to_screen(target))
        self.check_caught()

    def check_caught(self):
        if self.state == "playing" and self.player_tile == self.monster_tile:
            self.end("caught")

    # ---- Game loop ----------------------------------------------------------
    def tick(self):
        if self.state == "playing":
            now = time.time()
            if now >= self.end_time:
                self.end("timeout")
            else:
                if now - self.last_monster_move >= MONSTER_STEP:
                    self.last_monster_move = now
                    self.move_monster()
                self.monster.right(15)            # spin so it looks alive
                if self.state == "playing":
                    self.draw_hud()
        self.screen.update()
        self.screen.ontimer(self.tick, TICK_MS)

    def time_left(self):
        return max(0, self.end_time - time.time())

    def draw_hud(self):
        pen = self.hud_pen
        pen.clear()
        y = self.height / 2 - 15
        pen.color(STAR_COLOR)
        pen.goto(-self.width / 2, y)
        pen.write(f"★ Stars: {self.collected} / {STARS_NEEDED}", font=("Arial", 16, "bold"))

        seconds = int(self.time_left() + 0.999)
        pen.color(MONSTER_COLOR if seconds <= 10 else TEXT_COLOR)
        pen.goto(self.width / 2, y)
        pen.write(f"Time: {seconds // 60}:{seconds % 60:02d}", align="right",
                  font=("Arial", 16, "bold"))

    def end(self, result):
        self.state = result
        self.draw_hud()
        if result == "won":
            title, color = "MISSION COMPLETE!", STAR_COLOR
            used = TIME_LIMIT - self.time_left()
            detail = f"All {STARS_NEEDED} stars collected in {used:.1f} seconds"
        elif result == "caught":
            title, color = "CAUGHT BY THE MONSTER!", MONSTER_COLOR
            detail = f"You collected {self.collected} / {STARS_NEEDED} stars"
            self.player.color(MONSTER_COLOR)
        else:
            title, color = "TIME'S UP!", MONSTER_COLOR
            detail = f"You collected {self.collected} / {STARS_NEEDED} stars"

        pen = self.msg_pen
        pen.clear()
        # Dark box behind the message so it's readable over the maze.
        pen.goto(-230, 80)
        pen.color(BG)
        pen.begin_fill()
        for x, y in [(230, 80), (230, -60), (-230, -60), (-230, 80)]:
            pen.goto(x, y)
        pen.end_fill()

        pen.color(color)
        pen.goto(0, 25)
        pen.write(title, align="center", font=("Arial", 24, "bold"))
        pen.color(TEXT_COLOR)
        pen.goto(0, -5)
        pen.write(detail, align="center", font=("Arial", 14, "normal"))
        pen.goto(0, -40)
        pen.write("Press Space for a new maze", align="center", font=("Arial", 13, "italic"))


if __name__ == "__main__":
    MazeGame()
    turtle.mainloop()
