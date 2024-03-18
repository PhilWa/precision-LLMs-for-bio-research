import random


def update_grid(grid):
    new_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            new_grid[y][x] = next_state(x, y, grid)
    return new_grid


def next_state(x, y, grid):
    neighbors = count_neighbors(x, y, grid)
    if grid[y][x] == 1:
        return 1 if 2 <= neighbors <= 3 else 0
    else:
        return 1 if neighbors == 3 else 0


def count_neighbors(x, y, grid):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            count += grid[(y + i) % len(grid)][(x + j) % len(grid[0])]
    return count
