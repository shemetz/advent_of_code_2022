from typing import Dict, Set
import numpy as np

with open('day23.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

prev_elves: Set[complex] = set()
for r, line in enumerate(input_lines):
    for c, char in enumerate(line):
        if char == '#':
            elf = r * 1j + c
            prev_elves.add(elf)


# visualization
def draw_elf_map():
    min_e_x = min(int(e.real) for e in prev_elves)
    max_e_x = max(int(e.real) for e in prev_elves)
    min_e_y = min(int(e.imag) for e in prev_elves)
    max_e_y = max(int(e.imag) for e in prev_elves)
    elf_map = np.full((max_e_y - min_e_y + 1, max_e_x - min_e_x + 1), '.')
    for elff in prev_elves:
        elf_map[int(elff.imag - min_e_y), int(elff.real - min_e_x)] = '#'
    elf_map[- min_e_y, -min_e_x] = '╳'
    print('\n'.join(''.join(str(cell) for cell in row) for row in elf_map))


EIGHT_NEIGHBOR_DIRECTIONS = (-1 - 1j, -1, -1 + 1j, 0 - 1j, 0 + 1j, 1 - 1j, 1, 1 + 1j)
COMPASS = [-1j, +1j, -1, +1]
COMPASS_SIDES = [(+1 - 1j, 0 - 1j, -1 - 1j), (+1 + 1j, 0 + 1j, -1 + 1j), (+1j - 1, 0 - 1, -1j - 1),
                 (+1j + 1, 0 + 1, -1j + 1), ]
compass_phase = 0
# maps from current position to the previous locations of any proposing elf
# (only a maximum of 2 elves could propose moving to the same location!)
next_elf_spots: Dict[complex, complex] = {}
round_num = 0
lonelies_count = 999
while lonelies_count != len(prev_elves):
    lonelies_count = 0
    round_num += 1
    for elf in prev_elves:
        if all((elf + nearby_coord_delta) not in prev_elves for nearby_coord_delta in EIGHT_NEIGHBOR_DIRECTIONS):
            # stay in place because lonely
            next_elf_spots[elf] = elf  # (btw, no need to worry about incoming elves for elves who stay in place)
            lonelies_count += 1
            continue
        for phase_offset in range(4):
            attempted_phase = (compass_phase + phase_offset) % 4
            destination = elf + COMPASS[attempted_phase]
            for direction in COMPASS_SIDES[attempted_phase]:
                if elf + direction in prev_elves:
                    break
            else:  # did not break, which means it's an unblocked direction
                if destination in next_elf_spots:
                    # conflict found!  pushing other elf back, will be staying in place because conflict
                    other_elf_origin = next_elf_spots[destination]
                    del next_elf_spots[destination]
                    next_elf_spots[other_elf_origin] = other_elf_origin
                    # stay in place because conflict
                    next_elf_spots[elf] = elf
                    break
                # move (may move back later)
                next_elf_spots[destination] = elf
                break
        else:  # did not break, which means no unblocked direction was found
            # stay in place because blocked from all sides
            next_elf_spots[elf] = elf
    # move elves to their next locations
    prev_elves = set(next_elf_spots.keys())
    next_elf_spots.clear()
    compass_phase = (compass_phase + 1) % 4
    if round_num == 10:
        # calculate answer, by calculating size of area elves occupy and subtracting the elf count from it
        min_elf_x = min(int(e.real) for e in prev_elves)
        max_elf_x = max(int(e.real) for e in prev_elves)
        min_elf_y = min(int(e.imag) for e in prev_elves)
        max_elf_y = max(int(e.imag) for e in prev_elves)
        rectangle_area = (max_elf_x - min_elf_x + 1) * (max_elf_y - min_elf_y + 1)
        free_area_in_rectangle = rectangle_area - len(prev_elves)
        print(f"Part 1 solution: {free_area_in_rectangle}")  # 3864

print(f"Part 2 solution: {round_num}")  #
draw_elf_map()
