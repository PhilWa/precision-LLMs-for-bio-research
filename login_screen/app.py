from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# Set the initial game state
game_state = np.zeros((100, 250), dtype=bool)

import math


def init_random_groups(game_state, num_groups, group_size, radius):
    rows, cols = game_state.shape
    for _ in range(num_groups):
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        for _ in range(group_size):
            r = random.uniform(0, radius)
            angle = random.uniform(0, 2 * math.pi)
            dx, dy = int(r * math.cos(angle)), int(r * math.sin(angle))
            x, y = (x + dx) % rows, (y + dy) % cols
            game_state[x][y] = True


glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]

lwss = [[1, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 1]]

pulsar = [
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
]


def add_pattern(game_state, pattern, x, y):
    rows, cols = game_state.shape
    pattern_rows, pattern_cols = len(pattern), len(pattern[0])

    for i in range(pattern_rows):
        for j in range(pattern_cols):
            game_state[(x + i) % rows][(y + j) % cols] = pattern[i][j]


rows, cols = game_state.shape

num_groups = 5
group_size = 6
radius = 3
init_random_groups(game_state, num_groups, group_size, radius)

# Add interesting patterns at random locations
glider_x, glider_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
add_pattern(game_state, glider, glider_x, glider_y)
lwss_x, lwss_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
add_pattern(game_state, lwss, lwss_x, lwss_y)
pulsar_x, pulsar_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
add_pattern(game_state, pulsar, pulsar_x, pulsar_y)


def next_generation(game_state):
    next_state = game_state.copy()
    rows, cols = game_state.shape
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(game_state, i, j)
            if game_state[i][j]:
                if neighbors < 2 or neighbors > 3:
                    next_state[i][j] = False
            else:
                if neighbors == 3:
                    next_state[i][j] = True
    return next_state


def count_neighbors(game_state, x, y):
    rows, cols = game_state.shape
    return sum(
        game_state[(x + i) % rows][(y + j) % cols]
        for i in range(-1, 2)
        for j in range(-1, 2)
        if (i, j) != (0, 0)
    )


@app.route("/next", methods=["POST"])
def next():
    global game_state
    game_state = next_generation(game_state)
    return jsonify(game_state.tolist())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/toggle_cell", methods=["POST"])
def toggle_cell():
    global game_state
    x = int(request.form["x"])
    y = int(request.form["y"])
    game_state[x][y] = not game_state[x][y]
    return jsonify(success=True)


@app.route("/step")
def step():
    global game_state
    game_state = next_step(game_state)
    return jsonify(new_state=game_state.tolist())


def next_step(game_state):
    new_state = game_state.copy()
    rows, cols = game_state.shape
    for x in range(rows):
        for y in range(cols):
            neighbors = sum(
                game_state[(x + i) % rows][(y + j) % cols]
                for i in range(-1, 2)
                for j in range(-1, 2)
                if (i, j) != (0, 0)
            )
            if game_state[x][y]:
                if neighbors < 2 or neighbors > 3:
                    new_state[x][y] = False
            elif neighbors == 3:
                new_state[x][y] = True
    return new_state


@app.route("/add_random_group", methods=["POST"])
def add_random_group():
    global game_state
    x = int(request.form["x"])
    y = int(request.form["y"])
    group_size = 6
    radius = 3
    for _ in range(group_size):
        r = random.uniform(0, radius)
        angle = random.uniform(0, 2 * math.pi)
        dx, dy = int(r * math.cos(angle)), int(r * math.sin(angle))
        x, y = (x + dx) % game_state.shape[0], (y + dy) % game_state.shape[1]
        game_state[x][y] = True
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
