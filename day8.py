with open('day8.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

# idea:  pass left-to-right per column, maintaining highest seen so far.  anything that is equal or lower than it will be uncounted.
# need to avoid double counting!
# we'll keep a secondary data store for seen vs unseen.  a big 2D matrix

forest = [[int(c) for c in line] for line in input_lines]
width = len(forest[0])
height = len(forest)
visible = [[False for _ in range(width)] for _ in range(height)]

for y in range(height):
    # row by row, left to right
    tallest = -1
    for x in range(width):
        tree = forest[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True
    tallest = -1
    # row by row, right to left
    for x in reversed(range(width)):
        tree = forest[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True
for x in range(width):
    # column by column, top to bottom
    tallest = -1
    for y in range(height):
        tree = forest[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True
    # column by column, bottom to top
    tallest = -1
    for y in reversed(range(height)):
        tree = forest[y][x]
        if tree > tallest:
            tallest = tree
            visible[y][x] = True

# for line in visible:
#     print(''.join(str(int(c)) for c in line))
# converting bools into ints, summing them up
visible_count = sum(sum(int(c) for c in row) for row in visible)
print(visible_count)  # 1543

# part 2 - scenic scores
# optimization is lesser but still exists:  we'll track the most recent index of each tree height (only 10 possibilities),
# per pass.  so total number of checks is about 100 * 100 * 4 * 10
# each pass, we'll multiply each tree's position in the calculation grid by how many trees it sees to its left.
calculation_grid = [[1 for _ in range(width)] for _ in range(height)]
TEN = 10

for y in range(height):
    # row by row, left to right
    recentmost_per_height = [-999 for _ in range(TEN)]
    for x in range(width):
        tree_height = forest[y][x]
        recentmost_blocking = max(recentmost_per_height[tree_height:])
        viewing_distance = abs(x - recentmost_blocking) if recentmost_blocking != -999 else x
        calculation_grid[y][x] *= viewing_distance
        recentmost_per_height[tree_height] = x
    # row by row, right to left
    recentmost_per_height = [999 for _ in range(TEN)]
    for x in reversed(range(width)):
        tree_height = forest[y][x]
        recentmost_blocking = min(recentmost_per_height[tree_height:])
        viewing_distance = abs(x - recentmost_blocking) if recentmost_blocking != 999 else width - x - 1
        calculation_grid[y][x] *= viewing_distance
        recentmost_per_height[tree_height] = x
for x in range(width):
    # column by column, top to bottom
    recentmost_per_height = [-999 for _ in range(TEN)]
    for y in range(height):
        tree_height = forest[y][x]
        recentmost_blocking = max(recentmost_per_height[tree_height:])
        viewing_distance = abs(y - recentmost_blocking) if recentmost_blocking != -999 else y
        calculation_grid[y][x] *= viewing_distance
        recentmost_per_height[tree_height] = y
    # column by column, bottom to top
    recentmost_per_height = [999 for _ in range(TEN)]
    for y in reversed(range(height)):
        tree_height = forest[y][x]
        recentmost_blocking = min(recentmost_per_height[tree_height:])
        viewing_distance = abs(y - recentmost_blocking) if recentmost_blocking != 999 else height - y - 1
        calculation_grid[y][x] *= viewing_distance
        recentmost_per_height[tree_height] = y

# now we need to find the best one
best_scenic_score = max(max(scenic_score for scenic_score in row) for row in calculation_grid)
print(best_scenic_score)  # not 820800, too high

# TODO - refactor to have less copied code