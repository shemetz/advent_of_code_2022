import os
import random
import re
from time import sleep

import numpy as np

with open('day22.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

VOID = ' '
OPEN = '.'
WALL = '#'

instructions_str = input_lines[-1]
height = len(input_lines) - 2
board_strs = input_lines[:height]
width = max(len(line) for line in board_strs)
board = np.full((height, width), VOID)
for r, board_line in enumerate(board_strs):
    board[r:r + 1, 0:width] = list(board_line + ' ' * (width - len(board_line)))
if instructions_str[-1] not in 'RL':
    # string both started and ended with a movement.  hacky solution!
    instructions_str = instructions_str + 'R0L'  # add rotation right, move 0, rotation left
instructions = [re.fullmatch(r"(\d+)([RL])", match).groups() for match in re.findall(r"(\d+[RL])", instructions_str)]
instructions = [(int(pair[0]), -1 if pair[1] == 'L' else +1) for pair in instructions]
# print(instructions)
# print_board()

# starting position is top left open space we see, i.e. the first one in the input lines
position = (0, board_strs[0].index(OPEN))
facing = 0
board_by_facing = [
    np.rot90(board, k=0),  # = original board
    np.rot90(board, k=1),
    np.rot90(board, k=2),
    np.rot90(board, k=3),
]


def print_board():
    print('\n'.join(''.join(str(cell) for cell in row) for row in board))


def rot_position(k):
    width_prev, height_prev = board_by_facing[facing].shape
    curr_r, curr_c = position
    if k == +1:
        return height_prev - 1 - curr_c, curr_r
    if k == -1:
        return curr_c, width_prev - 1 - curr_r
    else:
        raise ValueError(f"k error {k}")


# print(position)
for instruction in instructions:
    distance, rotation_direction_number = instruction  # a number and then a +1/-1
    board_view = board_by_facing[facing]
    # print('\n'.join(''.join(str(cell) for cell in row) for row in board_view))
    # print(f'move {distance} then turn {rotation_direction_number}')
    for _ in range(distance):
        r, c = position
        position = (r, (c + 1) % board_view.shape[1])  # move forward as if we faced right
        thing = board_view[position]
        if thing == WALL:
            # move back
            position = (r, c)
            break
        if thing == VOID:
            # move forward step by step until not in a void anymore.  not optimized
            while board_view[position] == VOID:
                position = (r, (position[1] + 1) % board_view.shape[1])
            if board_view[position] == WALL:
                position = (r, c)
                break
        board_view[position] = '>v<^'[facing]
    # turn left or right
    # print(position, '-> ', end='')
    # print(position, facing)
    # print()
    position = rot_position(rotation_direction_number)
    facing = (facing + rotation_direction_number) % 4

final_facing = facing + 0
while facing != 0:
    position = rot_position(-1)
    facing -= 1

board[position] = '▇'
# print_board()
print(position, final_facing)

final_row = position[0] + 1
final_col = position[1] + 1
final_password = 1000 * final_row + 4 * final_col + final_facing
print("Part 1:", final_password)  # maybe 196134
# print(rot90position(*position, 0))
# print_board()
# print(rot90position(*position, 1))

print()
print()
print()

# PART 2 - resetting stuff
for r, board_line in enumerate(board_strs):
    board[r:r + 1, 0:width] = list(board_line + ' ' * (width - len(board_line)))
position = (0, board_strs[0].index(OPEN))
facing = 0


def print_3d_top_layer(cube_3d):
    print('\n'.join(''.join(str(cell[0]) for cell in row) for row in cube_3d))
    print('-------------')


def print_3d_all_layers(cube_3d):
    for z in range(cube_3d.shape[2]):
        print('\n'.join(''.join(str(cell[z]) for cell in row) for row in cube_3d))


region_size = max(width, height) // 4
big_cube_size = region_size + 2
orig_big_cube = np.full((big_cube_size, big_cube_size, big_cube_size), VOID)
big_cube = orig_big_cube
b = region_size + 1
s = region_size


def slice_face_view(region_x, region_y, transpose_maybe, rotation_count, shape):
    temp = board[region_x * s: region_x * s + s, region_y * s: region_y * s + s]
    if transpose_maybe:
        temp = temp.T
    temp = np.rot90(temp, k=rotation_count)
    return np.reshape(temp, shape)


def unslice_face_view(big_cube_area, transpose_maybe, rotation_count):
    """reverse what we did above to put it back on the board"""
    temp = np.reshape(big_cube_area, (region_size, region_size))
    temp = np.rot90(temp, k=-rotation_count)
    if transpose_maybe:
        temp = temp.T
    return temp


# lots of manual labor was done here
# TODO - fill up this big cube in some cleverer way
# helpers to orient myself
big_cube[0, 0, 0] = 1
big_cube[0, 0, b] = 2
big_cube[0, b, 0] = 3
big_cube[0, b, b] = 4
big_cube[b, 0, 0] = 5
big_cube[b, 0, b] = 6
big_cube[b, b, 0] = 7
big_cube[b, b, b] = 8
if region_size == 4:  # EXAMPLE INPUT
    big_cube[1:0 + b, 1:0 + b, 0:1 + 0] = slice_face_view(0, 2, False, 0, (s, s, 1))  # 1 3  5 7
    big_cube[b:1 + b, 1:0 + b, 1:0 + b] = slice_face_view(1, 2, True, 0, (1, s, s))  # 5 7  6 8
    big_cube[1:0 + b, 0:1 + 0, 1:0 + b] = slice_face_view(1, 1, True, 0, (s, 1, s))  # 1 5  2 6
    big_cube[0:1 + 0, 1:0 + b, 1:0 + b] = slice_face_view(1, 0, False, 1, (1, s, s))  # 4 3  2 1
    big_cube[1:0 + b, 1:0 + b, b:1 + b] = slice_face_view(2, 2, True, 1, (s, s, 1))  # 6 8  2 4
    big_cube[1:0 + b, b:1 + b, 1:0 + b] = slice_face_view(2, 3, False, 2, (s, 1, s))  # 8 7  4 3
else:  # MY REAL INPUT
    big_cube[1:0 + b, 1:0 + b, 0:1 + 0] = slice_face_view(0, 1, False, 0, (s, s, 1))  # 1 3  5 7
    big_cube[b:1 + b, 1:0 + b, 1:0 + b] = slice_face_view(1, 1, True, 0, (1, s, s))  # 5 7  6 8
    big_cube[1:0 + b, 0:1 + 0, 1:0 + b] = slice_face_view(2, 0, True, 1, (s, 1, s))  # 5 6  1 2
    big_cube[0:1 + 0, 1:0 + b, 1:0 + b] = slice_face_view(3, 0, False, 2, (1, s, s))  # 1 2  3 4
    big_cube[1:0 + b, 1:0 + b, b:1 + b] = slice_face_view(2, 1, True, 1, (s, s, 1))  # 6 8  2 4
    big_cube[1:0 + b, b:1 + b, 1:0 + b] = slice_face_view(0, 2, False, 0, (s, 1, s))  # 3 4  7 8


def fill_board_with_cube_faces():
    for r, board_line in enumerate(board_strs):
        board[r:r + 1, 0:width] = list(board_line + ' ' * (width - len(board_line)))
    if region_size == 4:  # EXAMPLE INPUT
        board[0 * s:0 * s + s, 2 * s:2 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 1:0 + b, 0:1 + 0], False, 0)
        board[1 * s:1 * s + s, 2 * s:2 * s + s] = unslice_face_view(orig_big_cube[b:1 + b, 1:0 + b, 1:0 + b], True, 0)
        board[1 * s:1 * s + s, 1 * s:1 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 0:1 + 0, 1:0 + b], True, 0)
        board[1 * s:1 * s + s, 0 * s:0 * s + s] = unslice_face_view(orig_big_cube[0:1 + 0, 1:0 + b, 1:0 + b], False, 1)
        board[2 * s:2 * s + s, 2 * s:2 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 1:0 + b, b:1 + b], True, 1)
        board[2 * s:2 * s + s, 3 * s:3 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, b:1 + b, 1:0 + b], False, 2)
    else:  # MY REAL INPUT
        board[0 * s:0 * s + s, 1 * s:1 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 1:0 + b, 0:1 + 0], False, 0)
        board[1 * s:1 * s + s, 1 * s:1 * s + s] = unslice_face_view(orig_big_cube[b:1 + b, 1:0 + b, 1:0 + b], True, 0)
        board[2 * s:2 * s + s, 0 * s:0 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 0:1 + 0, 1:0 + b], True, 1)
        board[3 * s:3 * s + s, 0 * s:0 * s + s] = unslice_face_view(orig_big_cube[0:1 + 0, 1:0 + b, 1:0 + b], False, 2)
        board[2 * s:2 * s + s, 1 * s:1 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, 1:0 + b, b:1 + b], True, 1)
        board[0 * s:0 * s + s, 2 * s:2 * s + s] = unslice_face_view(orig_big_cube[1:0 + b, b:1 + b, 1:0 + b], False, 0)


# print_3d_top_layer(np.rot90(big_cube, k=0, axes=(2, 1)))
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(2, 1)))
# print_3d_top_layer(np.rot90(big_cube, k=2, axes=(2, 1)))
# print_3d_top_layer(np.rot90(big_cube, k=3, axes=(2, 1)))
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(2, 0)))
# print_3d_top_layer(np.rot90(big_cube, k=3, axes=(2, 0)))

# print_3d_all_layers(big_cube)

# print_3d_top_layer(big_cube)
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(1, 0)))  # (1,0) rotates CW
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(0, 1)))  # (0,1) rotates CCW
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(2, 1)))  # (2, 1) rolls left
# print_3d_top_layer(np.rot90(big_cube, k=1, axes=(2, 0)))  # (2, 0) rolls forward


position_2d = (1, 1)  # (x, y, 0) - z will always stay 0


def rot_position_2d(k):
    curr_x, curr_y = position_2d
    if k == +1:
        return big_cube_size - 1 - curr_y, curr_x
    if k == -1:
        return curr_y, big_cube_size - 1 - curr_x
    else:
        raise ValueError(f"k error {k}")


def debug_print_step_and_wait():
    big_cube[position_2d[0], position_2d[1], 0] = '▇'
    fill_board_with_cube_faces()
    os.system('cls')
    print_board()
    sleep(0.01)
    big_cube[position_2d[0], position_2d[1], 0] = '.'
    print(f'instruction {inst_i}: {instruction}')


MARK_PATH = False
MARK_END_OF_PATH = True

big_cube[position_2d[0], position_2d[1], 0] = '╳'
# big_cube = np.rot90(big_cube, k=1, axes=(0, 1))
# position_2d = rot_position_2d(1)
# move across cube.  always assume we are on its top layer (x,y,0) and facing forwards (y -> infinity).
# cube will keep rotating to keep the above two things correct.

trail_letter = 'z'
# print_3d_top_layer(big_cube)
for inst_i, instruction in enumerate(instructions):
    trail_letter = chr(ord(trail_letter) + 1)
    if not trail_letter.isalpha():
        trail_letter = 'a'
    distance, rotation_direction_number = instruction  # a number and then a +1/-1
    for _ in range(distance):
        debug_print_step_and_wait()
        # print(f"Current position on top of cube: {position_2d}")
        x, y = position_2d
        position_2d = (x, y + 1)
        if y == big_cube_size - 2:
            # roll left and move x back to where it continues on this new face of the cube
            big_cube = np.rot90(big_cube, k=1, axes=(2, 1))
            position_2d = (x, 1)
            if big_cube[x, 1, 0] == WALL:
                # rolled into a wall, reverse it
                position_2d = (x, y)
                big_cube = np.rot90(big_cube, k=-1, axes=(2, 1))
                # print(f"Hit wall during rotation, new position_2d: {position_2d}")
                break
            # print(f"Rolled cube left, new position_2d: {position_2d}")
        elif big_cube[x, y + 1, 0] == WALL:
            # move back
            position_2d = (x, y)
            # print(f"Hit wall, new position_2d: {position_2d}")
            break
        if MARK_PATH:
            big_cube[position_2d[0], position_2d[1], 0] = trail_letter
        if MARK_END_OF_PATH and inst_i >= len(instructions) - 4:
            big_cube[position_2d[0], position_2d[1], 0] = '▒'  # marker for end of the path, to be able to see facing
        if MARK_END_OF_PATH and inst_i >= len(instructions) - 3:
            big_cube[position_2d[0], position_2d[1], 0] = 'O'  # marker for end of the path
    if MARK_END_OF_PATH and inst_i == len(instructions) - 1:
        big_cube[position_2d[0], position_2d[1] + 1, 0] = '¤'  # marker for past the end of the path
    # turn left or right
    position_2d = rot_position_2d(rotation_direction_number)
    # print(f"Turned {rotation_direction_number}, new position_2d: {position_2d}")
    big_cube = np.rot90(big_cube, k=rotation_direction_number, axes=(0, 1))
    # print_3d_top_layer(big_cube)
print('Finished moving around the cube.')
big_cube[position_2d[0], position_2d[1], 0] = '▇'
# rotate cube back
# (manually)

if region_size == 4:  # EXAMPLE INPUT
    final_facing = 3
else:  # MY REAL INPUT
    final_facing = 2

# print_3d_top_layer(big_cube)
fill_board_with_cube_faces()
print_board()
position = tuple(a[0] for a in (board == '▇').nonzero())
print(position, final_facing)
final_row = position[0] + 1
final_col = position[1] + 1
final_final_password = 1000 * final_row + 4 * final_col + final_facing
print("Part 2:", final_final_password)  # 123210 too low, 124210 too low, 126211 also too low
