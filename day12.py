import math
from typing import List, Tuple

import numpy as np

with open('day12.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


def char_to_num(c: str):
    if c == 'S':
        return 0
    if c == 'E':
        return 25
    return ord(c) - ord('a')  # a = 0, b = 1, c = 2, etc. and z = 25


heightmap_str_list = [[c for c in line] for line in input_lines]
heightmap_str = np.array(heightmap_str_list)
heightmap = np.vectorize(char_to_num, otypes=[int])(heightmap_str)
s_position = np.where(heightmap_str == 'S')
s_row = s_position[0][0]
s_col = s_position[1][0]
e_position = np.where(heightmap_str == 'E')
e_row = e_position[0][0]
e_col = e_position[1][0]
height = heightmap.shape[0]
width = heightmap.shape[1]

# doing pathfinding, from end to start/a, because of part 2
MARKER_NOT_VISITED = -1
distances_to_get_to_places = np.full(heightmap.shape, MARKER_NOT_VISITED)
frontier: List[Tuple[int, int]] = [(e_row, e_col)]
distances_to_get_to_places[e_row, e_col] = 0
found_closest_a_already = False
while frontier:
    row, col = frontier.pop(0)
    if heightmap_str[row, col] == 'S':
        print(f"Part 1, Reached S from E after distance: {distances_to_get_to_places[row, col]}")  # 412
        break  # breaking because parts 1+2 were done by now
    if not found_closest_a_already and heightmap_str[row, col] == 'a':
        print(f"Part 2, Reached a from E after distance: {distances_to_get_to_places[row, col]}")
        found_closest_a_already = True
    for delta_r, delta_c in [(-1, 0), (0, -1), (0, +1), (+1, 0)]:
        next_r, next_c = row + delta_r, col + delta_c
        # bounds check
        if 0 <= next_r < height and 0 <= next_c < width:
            # visited check
            if distances_to_get_to_places[next_r, next_c] == MARKER_NOT_VISITED:
                # altitude check
                if heightmap[next_r, next_c] >= heightmap[row, col] - 1:
                    next_position = (next_r, next_c)
                    frontier.append(next_position)
                    distances_to_get_to_places[next_r, next_c] = distances_to_get_to_places[row, col] + 1
