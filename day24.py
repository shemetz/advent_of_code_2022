import copy
import math
import numpy as np

with open('day24.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

valley_width = len(input_lines[0]) - 2
valley_height = len(input_lines) - 2
START_POSITION = 0 - 1j
END_POSITION = valley_width - 1 + 1j * valley_height
BIG_NUMBER = 999999999

blizzard_simulation_cache = {}


def simulate_next_blizzards_state(blizzards: tuple, time: int) -> tuple:
    # cycles after this much time
    # NOTE:  this cache is almost useless!  because real input has LCM=600 and parts 1+2 answers are about 300 and 900
    time_mod = time % math.lcm(valley_width, valley_height)
    if time_mod in blizzard_simulation_cache:
        return blizzard_simulation_cache[time_mod]
    next_blizzards_array = np.full((valley_height, valley_width), 0, dtype=complex)
    for r, line in enumerate(blizzards):
        for c, blizzes in enumerate(line):
            if int(blizzes.imag) in (-1, +1):
                next_blizzards_array[(r - 1) % valley_height, c] += -1j
            if int(blizzes.imag) in (+2, +1,):
                next_blizzards_array[(r + 1) % valley_height, c] += 2j
            if int(blizzes.real) in (-1, +1):
                next_blizzards_array[r, (c - 1) % valley_width] += -1
            if int(blizzes.real) in (+2, +1):
                next_blizzards_array[r, (c + 1) % valley_width] += 2
    next_blizzards_tuple = tuple(tuple(r for r in row) for row in next_blizzards_array)
    blizzard_simulation_cache[time_mod] = next_blizzards_tuple
    return next_blizzards_tuple


def print_state(blizzards: tuple, positions: list):
    positions_set = set(positions)
    for r, line in enumerate(blizzards):
        for c, blizzes in enumerate(line):
            char = {-1j: '^', -1: '<', +2j: 'v', +2: '>', +2: '>', 0: '.'}.get(blizzes, None)
            if char is None:
                cn = 0
                cn += 1 if blizzes.real != 0 else 0
                cn += 1 if blizzes.imag != 0 else 0
                cn += 1 if blizzes.real == +1 else 0
                cn += 1 if blizzes.imag == +1 else 0
                char = str(cn)
            if char == '.' and (r * 1j + c) in positions_set:
                char = 'E'
            print(char, end="")
        print()


def bfs_solve(start_position: complex, start_blizzards: tuple):
    start_pos, end_pos = start_position, END_POSITION
    time_passed = 0
    next_positions_set = set()
    positions = [start_position]
    blizzards = copy.deepcopy(start_blizzards)
    next_positions = []
    flipped_count = 0
    while True:
        # print_state(blizzards, positions)
        while positions:
            position = positions.pop(0)
            if position == end_pos:
                if flipped_count == 0:
                    print("Part 1 solution:", time_passed)  # 288
                if flipped_count < 2:
                    flipped_count += 1
                    start_pos, end_pos = end_pos, start_pos
                    positions = []
                    next_positions = []
                    next_positions_set = set()
                elif flipped_count == 2:
                    print("Part 2 solution:", time_passed)  # 861
                    return
            if position != start_pos:
                if not 0 <= position.real < valley_width or not 0 <= position.imag < valley_height:
                    continue
                if blizzards[int(position.imag)][int(position.real)] != 0:
                    continue
            for next_dir in (+1j, +1, 0, -1j, -1):
                next_position = position + next_dir
                if next_position not in next_positions_set:
                    next_positions.append(next_position)
                    next_positions_set.add(next_position)
        time_passed += 1
        blizzards = simulate_next_blizzards_state(blizzards, time_passed)
        positions = next_positions
        next_positions = []
        next_positions_set = set()
        # print(f"passed {time_passed}, len positions {len(positions)}")


def solve_parts():
    # keeping counts in single complex number, but two opposing blizzards are odd and even so it's ok
    blizzards_start_array = np.full((valley_height, valley_width), 0, dtype=complex)
    for r, line in enumerate(input_lines):
        for c, char in enumerate(line):
            blizz_dir = {'^': -1j, '<': -1, 'v': +2j, '>': +2, '.': 0, '#': 0}[char]
            if blizz_dir != 0:
                blizzards_start_array[r - 1, c - 1] += blizz_dir
    blizzards_start_tuple = tuple(tuple(r for r in row) for row in blizzards_start_array)

    bfs_solve(0 - 1j, blizzards_start_tuple)


solve_parts()
