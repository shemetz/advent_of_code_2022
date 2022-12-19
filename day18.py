import matplotlib.pyplot as plt
import numpy as np
import itertools

with open('day18.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

CUBE_SIZE = 23  # we manually found that the highest number is 21, we'll add 2 to have empty space around
# CUBE_SIZE = 8
AIR = 1
LAVA = 2
lava_cube_3d = np.full((CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), AIR)
for line in input_lines:
    x, y, z = [int(n) for n in line.split(',')]
    lava_cube_3d[x, y, z] = LAVA

# lava_cube_3d[2,1,4] = LAVA  # debugging

# test_cube_3d = np.full((2, 2, 2), 0)
# test_cube_3d[0,0,0] = 1
# test_cube_3d[0,0,1] = 2
# test_cube_3d[0,1,0] = 3
# test_cube_3d[0,1,1] = 4
# test_cube_3d[1,0,0] = 5
# lava_cube_3d = test_cube_3d

ROTATIONS_TO_1800 = [
    (0, 2),
    (1, 2),
    (0, 2),  # third one doesn't matter becasue we rotate at ends of loops
]

def count_surfaces(DIGIT_MARKING_OUTSIDE: int):
    cube_3d = np.copy(lava_cube_3d)
    total_surfaces_found = 0
    # count surface area per 1d line we can pass through
    for rotation_axes in ROTATIONS_TO_1800:
        for x, y in itertools.product(range(CUBE_SIZE), range(CUBE_SIZE)):
            in_or_out = False  # true when inside a lava voxel
            switch_count = 0
            for z in range(CUBE_SIZE):
                voxel_is_lava = cube_3d[x, y, z] != DIGIT_MARKING_OUTSIDE
                if in_or_out != voxel_is_lava:
                    in_or_out = not in_or_out
                    switch_count += 1
            total_surfaces_found += switch_count
        # we'll rotate the cube 90 degrees 3 times to cover all angles
        cube_3d = np.rot90(cube_3d, 1, rotation_axes)
        # print(cube_3d, end='\n-------\n')
    return total_surfaces_found


lava_to_air_surfaces = count_surfaces(AIR)
print('Part 1 solution:', lava_to_air_surfaces)  # 4310

# flood fill with smoke on the outside
SMOKE = 5
flood_frontier = [(0, 0, 0)]
while flood_frontier:
    vox = flood_frontier.pop(0)
    x, y, z = vox
    if not 0 <= x < CUBE_SIZE or not 0 <= y < CUBE_SIZE or not 0 <= z < CUBE_SIZE:
        continue
    if lava_cube_3d[vox] != AIR:
        continue
    lava_cube_3d[vox] = SMOKE
    flood_frontier.append((x + 1, y + 0, z + 0))
    flood_frontier.append((x - 1, y + 0, z + 0))
    flood_frontier.append((x + 0, y + 1, z + 0))
    flood_frontier.append((x + 0, y - 1, z + 0))
    flood_frontier.append((x + 0, y + 0, z + 1))
    flood_frontier.append((x + 0, y + 0, z - 1))

lava_to_smoke = count_surfaces(SMOKE)
print('Part 2 solution:', lava_to_smoke)  # 2466

# visualization of lava drop
COLORS = {
    LAVA: '#ff000022',
    AIR: '#00ff0066',  # can't render for some reason, matplotlib is annoying
    SMOKE: '#11111102',
}
colors_3d = np.vectorize(COLORS.get)(lava_cube_3d)
ax = plt.figure().add_subplot(projection='3d')
non_smokes = np.where(lava_cube_3d != SMOKE, True, False)
ax.voxels(non_smokes, facecolors=colors_3d, edgecolor='#00000022', shade=True)

plt.show()
