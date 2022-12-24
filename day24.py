import math
import numpy as np

"""
CORE ALGORITHM IDEAS:

1. to track blizzards, keep them in a numpy array where each grid square is 4 bits, one per blizzard direction.
no more than one blizzard per direction can be in a single location (due to how they were created) so it's good.
if e.g. one up-facing blizzard and one right-facing blizzard both occupy the same space, that space's bits will be 1001.

2. pathfinding is done in a BFS-like fashion, where I maintain a set of ALL current positions and ALL next positions,
along with a time counter.  each big loop, I use positions to calculate all legal next_positions, and then tick time.
a solution will be found when one of the positions reaches the goal.

3. for part 2, when reaching the exit I destroy all other positions and exchange the goals, and then repeat it later.
"""

with open('day24.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

valley_width = len(input_lines[0]) - 2
valley_height = len(input_lines) - 2
TOP_LEFT_VALLEY_OPENING = 0 - 1j
BOTTOM_RIGHT_VALLEY_OPENING = valley_width - 1 + 1j * valley_height
blizzard_simulation_cache = {}


def init_blizzards():
    blizzards_start_array = np.full((valley_height, valley_width), 0)
    for row_i, line in enumerate(input_lines):
        for col_i, char in enumerate(line):
            # ignoring the sides of the valley
            row, col = row_i - 1, col_i - 1
            if 0 <= row < valley_height and 0 <= col < valley_width:
                blizz_dir = {'>': +1, 'v': +2, '<': +4, '^': +8, '.': 0, '#': 0}[char]
                blizzards_start_array[row, col] += blizz_dir
    return blizzards_start_array


def simulate_next_blizzards_state(blizzards: np.ndarray, time: int) -> np.ndarray:
    # cycles after this much time
    # NOTE:  this cache is almost useless!  because real input has LCM=600 and parts 1+2 answers are about 300 and 900
    time_mod = time % math.lcm(valley_width, valley_height)
    if time_mod in blizzard_simulation_cache:
        return blizzard_simulation_cache[time_mod]
    next_blizzards_array = np.full((valley_height, valley_width), 0)
    for row, line in enumerate(blizzards):
        for col, blizz_bits in enumerate(line):
            next_blizzards_array[(row + 0) % valley_height, (col + 1) % valley_width] += blizz_bits & 1
            next_blizzards_array[(row + 1) % valley_height, (col + 0) % valley_width] += blizz_bits & 2
            next_blizzards_array[(row + 0) % valley_height, (col - 1) % valley_width] += blizz_bits & 4
            next_blizzards_array[(row - 1) % valley_height, (col + 0) % valley_width] += blizz_bits & 8
    blizzard_simulation_cache[time_mod] = next_blizzards_array
    return next_blizzards_array


def print_state(blizzards: np.ndarray, positions: set):
    print()
    print('#' + ('E' if TOP_LEFT_VALLEY_OPENING in positions else '.') + '#' * valley_width)
    for r, line in enumerate(blizzards):
        print('#', end="")
        for c, blizz_bits in enumerate(line):
            char = {+1: '>', +2: 'v', +4: '<', +8: '^', 0: '.'}.get(blizz_bits)
            if char is None:
                cn = 0
                cn += (blizz_bits & 1) // 1
                cn += (blizz_bits & 2) // 2
                cn += (blizz_bits & 4) // 4
                cn += (blizz_bits & 8) // 8
                char = str(cn)
            if char == '.' and (r * 1j + c) in positions:
                char = 'E'
            print(char, end="")
        print('#', end="")
        print()
    print('#' * valley_width + ('E' if BOTTOM_RIGHT_VALLEY_OPENING in positions else '.') + '#')


def bfs_solve(start_position: complex, blizzards: np.ndarray):
    time_passed = 0
    positions = {start_position}
    next_positions = set()
    start_pos, end_pos = start_position, BOTTOM_RIGHT_VALLEY_OPENING
    flipped_count = 0
    while True:
        # print_state(blizzards, positions)
        blizzards = simulate_next_blizzards_state(blizzards, time_passed)
        while positions:
            position = positions.pop()
            if position == end_pos:
                if flipped_count == 0:
                    print("Part 1 solution:", time_passed)  # 288
                if flipped_count < 2:
                    flipped_count += 1
                    start_pos, end_pos = end_pos, start_pos
                    positions = set()
                    next_positions = set()
                elif flipped_count == 2:
                    print("Part 2 solution:", time_passed)  # 861
                    return
            for next_dir in (+1j, +1, 0, -1j, -1):
                next_position = position + next_dir
                if next_position != start_pos and next_position != end_pos:
                    if not 0 <= next_position.real < valley_width or not 0 <= next_position.imag < valley_height:
                        # hit sides of valley
                        continue
                    if blizzards[int(next_position.imag)][int(next_position.real)] != 0:
                        # hit blizzard
                        continue
                if next_position not in next_positions:
                    next_positions.add(next_position)
        time_passed += 1
        positions = next_positions
        next_positions = set()


def solve_parts():
    bfs_solve(0 - 1j, init_blizzards())


solve_parts()
