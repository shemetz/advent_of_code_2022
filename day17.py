import numpy as np

with open('day17.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

jets = ['<_>'.index(c) - 1 for c in input_lines[0]]
ROCK_SHAPES = [
    np.matrix([
        [1, 1, 1, 1, ],
    ]),
    np.matrix([
        [0, 1, 0, ],
        [1, 1, 1, ],
        [0, 1, 0, ],
    ]),
    np.matrix([
        [0, 0, 1, ],
        [0, 0, 1, ],
        [1, 1, 1, ],
    ]),
    np.matrix([
        [1, ],
        [1, ],
        [1, ],
        [1, ],
    ]),
    np.matrix([
        [1, 1, ],
        [1, 1, ],
    ]),
]
ROCK_MATTER = '#'
AIR_MATTER = '.'
PIT_WIDTH = 7
ROCKS_TO_SIMULATE_FOR_PART_1 = 2022
ROCKS_TO_SIMULATE_FOR_PART_2 = 1000000000000


def check_bump(top_left_x, top_left_y, rock_matrix, pit) -> bool:
    rock_height, rock_width = rock_matrix.shape
    area_height, area_width = pit.shape
    # check bounds
    if not 0 <= top_left_x <= area_width - rock_width:
        return True
    if not 0 <= top_left_y <= area_height - rock_height:
        return True
    # check collision
    subpit = pit[top_left_y:top_left_y+rock_height, top_left_x:top_left_x+rock_width]
    collisions = np.logical_and(subpit, rock_matrix)
    return np.any(collisions)  # True if at least two 1s collided in the same place


def solve_parts_a_and_b():
    signatures_to_samples = dict()
    pit_height = 2 * ROCKS_TO_SIMULATE_FOR_PART_1
    pit_height *= 200  # this is enough to stop a cycle, after manually trying
    pit = np.full((pit_height, PIT_WIDTH), 0)  # 0s for air, 1s for rock
    jets_generated = 0
    rocks_generated = 0
    topmost_y = pit_height
    tower_height_of_skip = 0
    did_find_a_cycle = False
    occasional_mod_to_check = -1

    while rocks_generated < ROCKS_TO_SIMULATE_FOR_PART_2:
        rock_matrix = ROCK_SHAPES[rocks_generated % len(ROCK_SHAPES)]
        rocks_generated += 1
        rock_height, rock_width = rock_matrix.shape
        # create rock in place.  x and y are rock shapes' top left corner
        x = 2
        y = topmost_y - 3 - rock_height
        while True:  # loop breaks after every collision
            # move horizontally
            jet_dir_num = jets[jets_generated % len(jets)]
            jets_generated += 1
            x += jet_dir_num
            # check bump
            if check_bump(x, y, rock_matrix, pit):
                x -= jet_dir_num
            # move down
            y += 1
            # check bump
            if check_bump(x, y, rock_matrix, pit):
                y -= 1
                # stop to rest
                pit[y:y+rock_height, x:x+rock_width] = np.logical_or(rock_matrix, pit[y:y+rock_height, x:x+rock_width])
                topmost_y = min(topmost_y, y)
                break
        if rocks_generated == ROCKS_TO_SIMULATE_FOR_PART_1:
            print('Part 1:', pit_height - topmost_y)  # 3085
            occasional_mod_to_check = jets_generated % len(jets)
        if jets_generated % len(jets) == occasional_mod_to_check:
            print(f'checked, after {rocks_generated} rocks and {jets_generated} jets')
            topology_signature_height = 1
            topology = hash(str(pit[topmost_y:topmost_y + topology_signature_height, 0: PIT_WIDTH].data))
            signature = (
                jets_generated % len(jets),
                rocks_generated % len(ROCK_SHAPES),
                topology,
            )
            sample = (
                jets_generated,
                rocks_generated,
                topmost_y,
            )
            if not did_find_a_cycle and signature in signatures_to_samples:
                # omg we found a cycle
                prev_sample = signatures_to_samples[signature]
                print('found cycle!')
                prev_jets, prev_rocks, prev_top_y = prev_sample
                cycle_rock_count = rocks_generated - prev_rocks
                cycle_height_added = -(topmost_y - prev_top_y)
                skippable_rock_count = ROCKS_TO_SIMULATE_FOR_PART_2 - rocks_generated
                skipped_cycles_count = skippable_rock_count // cycle_rock_count  # rounded down
                rocks_generated += skipped_cycles_count * cycle_rock_count
                tower_height_of_skip = skipped_cycles_count * cycle_height_added
                print(f'cycle rock count: {cycle_rock_count}.  skipping {skipped_cycles_count} cycles')
                did_find_a_cycle = True
            signatures_to_samples[signature] = sample
    print('Part 2:', tower_height_of_skip + (pit_height - topmost_y))  # 1535483870924


solve_parts_a_and_b()
