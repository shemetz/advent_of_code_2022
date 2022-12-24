# credit to 4HbQ whose code I edited a little to be more readable to me.  also added part 1.
# https://www.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/j17k7nn/

import re

FACING_LETTERS = {+1j: '>', +1: 'v', -1j: '<', -1: '^'}


def wrap_2d_example(pos, facing):
    # __@_
    # @@@_
    # __@@
    rs = 4
    x, y = pos.real, pos.imag
    xmod, ymod = x % rs, y % rs
    prev_x, prev_y = pos.real - facing.real, pos.imag - facing.imag
    match prev_x//rs, prev_y//rs, facing:
        case 0, 2, 1.j: return complex(x, 2*rs+ymod), facing
        case 1, 2, 1.j: return complex(x, 0*rs+ymod), facing
        case 2, 3, 1.j: return complex(x, 2*rs+ymod), facing
        case 0, 2, -1j: return complex(x, 2*rs+ymod), facing
        case 1, 0, -1j: return complex(x, 2*rs+ymod), facing
        case 2, 2, -1j: return complex(x, 3*rs+ymod), facing
        case 1, 0, 1.0: return complex(1*rs+xmod, y), facing
        case 1, 1, 1.0: return complex(1*rs+xmod, y), facing
        case 2, 2, 1.0: return complex(0*rs+xmod, y), facing
        case 2, 3, 1.0: return complex(2*rs+xmod, y), facing
        case 1, 0, -1.: return complex(1*rs+xmod, y), facing
        case 1, 1, -1.: return complex(1*rs+xmod, y), facing
        case 0, 2, -1.: return complex(2*rs+xmod, y), facing
        case 2, 3, -1.: return complex(2*rs+xmod, y), facing


def wrap_3d_example(pos, facing):
    rs = 4
    x, y = pos.real, pos.imag
    xmod, ymod = x % rs, y % rs
    xrev, yrev = rs - xmod - 1, rs - ymod - 1
    left, top_, rght, bttm = 0, 0, rs-1, rs-1
    prev_x, prev_y = pos.real - facing.real, pos.imag - facing.imag
    match prev_x//rs, prev_y//rs, facing:
        case 0, 2, 1.j: return complex(2, 3) * rs + complex(xrev, rght), -1j
        case 1, 2, 1.j: return complex(2, 3) * rs + complex(top_, xrev), +1.
        case 2, 3, 1.j: return complex(0, 2) * rs + complex(xrev, rght), -1j
        case 0, 2, -1j: return complex(1, 1) * rs + complex(top_, xrev), +1.
        case 1, 0, -1j: return complex(3, 4) * rs + complex(bttm, xrev), -1j
        case 2, 2, -1j: return complex(1, 1) * rs + complex(bttm, xrev), -1.
        case 1, 0, 1.0: return complex(2, 2) * rs + complex(bttm, yrev), -1.
        case 1, 1, 1.0: return complex(2, 2) * rs + complex(yrev, left), +1j
        case 2, 2, 1.0: return complex(1, 0) * rs + complex(bttm, yrev), -1.
        case 2, 3, 1.0: return complex(1, 0) * rs + complex(yrev, left), +1j
        case 1, 0, -1.: return complex(0, 2) * rs + complex(top_, yrev), +1.
        case 1, 1, -1.: return complex(0, 2) * rs + complex(ymod, left), 1j
        case 0, 2, -1.: return complex(1, 0) * rs + complex(top_, yrev), +1j
        case 2, 3, -1.: return complex(1, 2) * rs + complex(yrev, rght), -1j


def wrap_2d_actual(pos, facing):
    # _@@
    # _@_
    # @@_
    # @__
    rs = 50
    x, y = pos.real, pos.imag
    xmod, ymod = x % rs, y % rs
    prev_x, prev_y = pos.real - facing.real, pos.imag - facing.imag
    match prev_x//rs, prev_y//rs, facing:
        case 0, 2, 1.j: return complex(prev_x, 1*rs+ymod), facing
        case 1, 1, 1.j: return complex(prev_x, 1*rs+ymod), facing
        case 2, 1, 1.j: return complex(prev_x, 0*rs+ymod), facing
        case 3, 0, 1.j: return complex(prev_x, 0*rs+ymod), facing
        case 0, 1, -1j: return complex(prev_x, 2*rs+ymod), facing
        case 1, 1, -1j: return complex(prev_x, 1*rs+ymod), facing
        case 2, 0, -1j: return complex(prev_x, 1*rs+ymod), facing
        case 3, 0, -1j: return complex(prev_x, 0*rs+ymod), facing
        case 3, 0, 1.0: return complex(2*rs+xmod, prev_y), facing
        case 2, 1, 1.0: return complex(0*rs+xmod, prev_y), facing
        case 0, 2, 1.0: return complex(0*rs+xmod, prev_y), facing
        case 2, 0, -1.: return complex(3*rs+xmod, prev_y), facing
        case 0, 1, -1.: return complex(2*rs+xmod, prev_y), facing
        case 0, 2, -1.: return complex(0*rs+xmod, prev_y), facing


def wrap_3d_actual(pos, facing):
    rs = 50
    x, y = pos.real, pos.imag
    prev_x, prev_y = pos.real - facing.real, pos.imag - facing.imag
    xmod, ymod = x % rs, y % rs
    xrev, yrev = rs - xmod - 1, rs - ymod - 1
    left, top_, rght, bttm = 0, 0, rs-1, rs-1
    match prev_x//rs, prev_y//rs, facing:
        case 0, 2, 1.j: return complex(2, 1) * rs + complex(xrev, rght), -1j
        case 1, 1, 1.j: return complex(0, 2) * rs + complex(bttm, xmod), -1.
        case 2, 1, 1.j: return complex(0, 2) * rs + complex(xrev, rght), -1j
        case 3, 0, 1.j: return complex(2, 1) * rs + complex(bttm, xmod), -1.
        case 0, 1, -1j: return complex(2, 0) * rs + complex(xrev, left), +1j
        case 1, 1, -1j: return complex(2, 0) * rs + complex(top_, xmod), +1
        case 2, 0, -1j: return complex(0, 1) * rs + complex(xrev, left), +1j
        case 3, 0, -1j: return complex(0, 1) * rs + complex(top_, xmod), +1.
        case 3, 0, 1.0: return complex(0, 2) * rs + complex(top_, ymod), +1.
        case 2, 1, 1.0: return complex(3, 0) * rs + complex(ymod, rght), -1j
        case 0, 2, 1.0: return complex(1, 1) * rs + complex(ymod, rght), -1j
        case 2, 0, -1.: return complex(1, 1) * rs + complex(ymod, left), +1j
        case 0, 1, -1.: return complex(3, 0) * rs + complex(ymod, left), +1j
        case 0, 2, -1.: return complex(3, 0) * rs + complex(bttm, ymod), -1.


def print_grid(grid, pos):
    height, width = max(int(p.real) for p in grid), max(int(p.imag) for p in grid)
    for x in range(height):
        for y in range(width):
            if pos == (x + y * 1j):
                print('E', end="")
            else:
                print(grid.get(x + y * 1j, ' '), end="")
        print()


def solve_x(filename, wrap_func):
    *grid, _, path = open(filename)
    # grid[x+y*1j] is grid at row x column y.
    # facing is +1j when going right, +1 down, -1j left, -1 up.
    start_pos, start_facing = grid[0].index('.') * 1j, 1j
    grid = {(x+y*1j): c for x, l in enumerate(grid) for y, c in enumerate(l) if c in '.#'}
    pos, facing = start_pos, start_facing
    for move in re.findall(r'\d+|[RL]', path):
        # print_grid(grid, pos)
        match move:
            case 'L':
                facing *= +1j
            case 'R':
                facing *= -1j
            case _:
                for _ in range(int(move)):
                    grid[pos] = FACING_LETTERS[facing]
                    p, f = pos + facing, facing
                    if p not in grid:
                        p, f = wrap_func(p, f)
                    if grid[p] == '#':
                        break
                    else:
                        pos, facing = p, f
    password_s1 = 1000 * (pos.real+1)
    password_s2 = 4 * (pos.imag+1)
    password_s3 = [1j, 1, -1j, -1].index(facing)
    return int(password_s1 + password_s2 + password_s3)


print('Example Part 1:', solve_x('day22_example.txt', wrap_2d_example))  # 6032
print('Example Part 2:', solve_x('day22_example.txt', wrap_3d_example))  # 5031
print('Part 1:', solve_x('day22.txt', wrap_2d_actual))  # 196134
print('Part 2:', solve_x('day22.txt', wrap_3d_actual))  # 146011
