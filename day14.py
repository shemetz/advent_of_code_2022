from typing import Tuple, List

import numpy as np

with open('day14.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

Point = Tuple[int, int]
SAND_ORIGIN = (500, 0)
SAND_SOURCE = '+'
AIR = ' '
ROCK = '▇'
SAND = '▒'
# generate cave
cave_paths: List[List[Point]] = []
min_x, min_y, max_x, max_y = 500, 0, 500, 0  # initial values before expanding range
for line in input_lines:
    points_strs = line.split(' -> ')
    path: List[Point] = []
    for point_str in points_strs:
        x, y = [int(number) for number in point_str.split(',')]
        path.append((x, y))
        min_x, min_y, max_x, max_y = min(min_x, x), min(min_y, y), max(max_x, x), max(max_y, y)
    cave_paths.append(path)
max_x += 1
max_y += 1
print('bounds:')
print(min_x, min_y, 'to', max_x, max_y)
print('shifting all input to have saner bounds')
cave_paths = [[(point[0] - min_x, point[1] - min_y) for point in path] for path in cave_paths]
SAND_ORIGIN = (SAND_ORIGIN[0] - min_x, SAND_ORIGIN[1] - min_y)
min_x, min_y, max_x, max_y = 0, 0, max_x - min_x, max_y - min_y
print('new bounds:')
print(min_x, min_y, 'to', max_x, max_y)
print('sand origin at', SAND_ORIGIN)
cave = np.full((max_x, max_y), AIR)


# fill it up
def generate_cave():
    for path in cave_paths:
        for i in range(1, len(path)):
            prev_point = path[i - 1]
            next_point = path[i]
            left_x = min(prev_point[0], next_point[0])
            right_x = max(prev_point[0], next_point[0])
            top_y = min(prev_point[1], next_point[1])
            bottom_y = max(prev_point[1], next_point[1])
            cave[left_x:right_x + 1, top_y:bottom_y + 1] = ROCK
    cave[SAND_ORIGIN] = SAND_SOURCE


generate_cave()

# simulate
active_sand = SAND_ORIGIN
while True:
    x, y = active_sand
    if y + 1 == max_y:
        # falling down out of bounds
        break
    if cave[x, y + 1] == AIR:
        active_sand = (x, y + 1)
    elif x == min_x:
        # falling down-left out of bounds
        break
    elif cave[x - 1, y + 1] == AIR:
        active_sand = (x - 1, y + 1)
    elif x + 1 == max_x:
        # falling down-right out of bounds
        break
    elif cave[x + 1, y + 1] == AIR:
        active_sand = (x + 1, y + 1)
    else:  # needs to rest
        cave[active_sand] = SAND
        active_sand = SAND_ORIGIN

print('Part 1 solution:', (cave == SAND).sum())

# visualization
print('\n'.join(''.join(str(cell) for cell in row) for row in cave.transpose()))

print('Simulating part 2 now...')

print('bounds:')
print(min_x, min_y, 'to', max_x, max_y)
print('shifting all input to have saner bounds')
max_y += 2
min_x = SAND_ORIGIN[0] - max_y - 1
max_x = SAND_ORIGIN[0] + max_y + 1
cave_paths = [[(point[0] - min_x, point[1] - min_y) for point in path] for path in cave_paths]
SAND_ORIGIN = (SAND_ORIGIN[0] - min_x, SAND_ORIGIN[1] - min_y)
min_x, min_y, max_x, max_y = 0, 0, max_x - min_x, max_y - min_y
print('new bounds:')
print(min_x, min_y, 'to', max_x, max_y)
print('sand origin at', SAND_ORIGIN)
cave = np.full((max_x, max_y), AIR)
generate_cave()
cave[min_x:max_x, max_y - 1:max_y] = ROCK

# simulate
active_sand = SAND_ORIGIN
while True:
    x, y = active_sand
    if cave[x, y + 1] == AIR:
        active_sand = (x, y + 1)
    elif cave[x - 1, y + 1] == AIR:
        active_sand = (x - 1, y + 1)
    elif cave[x + 1, y + 1] == AIR:
        active_sand = (x + 1, y + 1)
    else:  # needs to rest
        cave[active_sand] = SAND
        if active_sand == SAND_ORIGIN:
            break
        active_sand = SAND_ORIGIN

print('Part 2 solution:', (cave == SAND).sum())  # 25193
# visualization
print('\n'.join(''.join(str(cell) for cell in row) for row in cave.transpose()))
