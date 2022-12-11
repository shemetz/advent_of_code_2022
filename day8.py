with open('day8.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

# idea:  pass left-to-right per column, maintaining highest seen so far.  anything that is equal or lower than it will be uncounted.
# need to avoid double counting!
# we'll keep a secondary data store for seen vs unseen.  a big 2D matrix

forest = [[int(c) for c in line] for line in input_lines]
width = len(forest[0])
height = len(forest)
visibility_calculation_grid = [[False for _ in range(width)] for _ in range(height)]


def calc_one_directional_visibility(upper_index, is_row_or_col, width_or_height, is_reversed):
    lower_index_range = range(width_or_height)
    if is_reversed:
        lower_index_range = reversed(lower_index_range)
    tallest = -1
    for lower_index in lower_index_range:
        tree = forest[upper_index][lower_index] if is_row_or_col else forest[lower_index][upper_index]
        if tree > tallest:
            tallest = tree
            if is_row_or_col:
                visibility_calculation_grid[upper_index][lower_index] = True
            else:
                visibility_calculation_grid[lower_index][upper_index] = True


def run_function_once_per_grid_direction(func):
    for y in range(height):
        # row by row, left to right
        func(y, True, width, False)
        # row by row, right to left
        func(y, True, width, True)
    for x in range(width):
        # column by column, top to bottom
        func(x, False, height, False)
        # column by column, bottom to top
        func(x, False, height, True)


run_function_once_per_grid_direction(calc_one_directional_visibility)
visible_count = sum(sum(int(c) for c in row) for row in visibility_calculation_grid)
print(visible_count)  # 1543

# part 2 - scenic scores
# optimization is lesser but still exists:  we'll track the most recent index of each tree height (only 10 possibilities),
# per pass.  so total number of checks is about 100 * 100 * 4 * 10
# each pass, we'll multiply each tree's position in the calculation grid by how many trees it sees to its left.
viewing_distance_calculation_grid = [[1 for _ in range(width)] for _ in range(height)]
TEN = 10


def calc_one_directional_viewing_distances(upper_index, is_row_or_col, width_or_height, is_reversed):
    lower_index_range = range(width_or_height)
    if is_reversed:
        lower_index_range = reversed(lower_index_range)
    edge_marker = width_or_height if is_reversed else -1
    recentmost_per_height = [edge_marker for _ in range(TEN)]
    max_or_min = min if is_reversed else max
    for lower_index in lower_index_range:
        tree_height = forest[upper_index][lower_index] if is_row_or_col else forest[lower_index][upper_index]
        recentmost_blocking = max_or_min(recentmost_per_height[tree_height:])
        viewing_distance = abs(lower_index - recentmost_blocking) if recentmost_blocking != edge_marker else (
            width_or_height - lower_index - 1 if is_reversed else lower_index
        )
        if is_row_or_col:
            viewing_distance_calculation_grid[upper_index][lower_index] *= viewing_distance
        else:
            viewing_distance_calculation_grid[lower_index][upper_index] *= viewing_distance
        recentmost_per_height[tree_height] = lower_index


run_function_once_per_grid_direction(calc_one_directional_viewing_distances)
# now we need to find the best one
best_scenic_score = max(max(scenic_score for scenic_score in row) for row in viewing_distance_calculation_grid)
print(best_scenic_score)  # 595080
