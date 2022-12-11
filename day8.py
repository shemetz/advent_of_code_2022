import numpy as np

with open('day8.txt') as input_file:
    input_lines = input_file.readlines()
# idea:  pass left-to-right per column, maintaining highests seen so far.
# this code even supports non-square grids!  as long as all trees are within the 0-9 height range
EDGE_MARKER = -1
TEN = 10
forest_chars = [[c for c in line.strip()] for line in input_lines]
original_forest: np.ndarray = np.array(forest_chars, dtype=int)
# seen = 1, unseen = 0.  can only go up (enough to be visible in 1 direction)
visibility_array = np.full(original_forest.shape, 0)
# this calculation array will have the product of viewing distances for each direction checked so far.
# numbers multiplied over time, will be 0s for edges
scenic_score_calculation_array = np.full(original_forest.shape, 1)
for rotation_count in range(4):
    # to be very clever, we rotate the entire forest by 90 degrees four times, to get each direction.
    # this way we don't need to think about up/down/left/right, we just think about right/right/right/right.
    rotated_forest = np.rot90(original_forest, k=rotation_count)  # k=1 rotates 90 deg counterclockwise, k=2 -> 180, etc
    rotated_visibility_grid = np.rot90(visibility_array, k=rotation_count)
    rotated_scenic_score_grid = np.rot90(scenic_score_calculation_array, k=rotation_count)
    width, height = rotated_forest.shape
    for y in range(height):
        tallest = -1
        latest_per_height = np.full(TEN, EDGE_MARKER)  # for each height, contains latest index of such a high tree
        for x in range(width):
            tree_height = rotated_forest[y][x]
            rotated_visibility_grid[y][x] = max(rotated_visibility_grid[y][x], int(tree_height > tallest))
            tallest = max(tallest, tree_height)
            latest_blocking = max(latest_per_height[tree_height:])  # note the range: not comparing to shorter trees
            latest_per_height[tree_height] = x
            viewing_distance = x - latest_blocking if latest_blocking != EDGE_MARKER else x
            rotated_scenic_score_grid[y][x] *= viewing_distance
# NOTE: when numpy edits a rotated copy, it affects the original too!  so this will work!
visible_count = visibility_array.sum()
print(visible_count)  # 1543
best_scenic_score = scenic_score_calculation_array.max(None, None, False, -1)  # just max(), but this avoids a warning
print(best_scenic_score)  # 595080
