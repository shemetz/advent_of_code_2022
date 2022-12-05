import copy
import re

with open('day5.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

stack_numbering_index = -1
for i, line in enumerate(input_lines):
    if '[' not in line:
        stack_numbering_index = i
        break

num_of_stacks = int(input_lines[stack_numbering_index].strip().split(' ')[-1])
orig_stacks = [[]] + [[] for _ in range(num_of_stacks)]  # extra empty stack is first
for stack_i in range(1, num_of_stacks + 1):
    for height in range(0, stack_numbering_index):
        y_coord = stack_numbering_index - 1 - height
        x_coord = 4 * (stack_i - 1) + 1
        if x_coord > len(input_lines[y_coord]):
            # spaces at end of line were stripped
            break
        crate_letter = input_lines[y_coord][x_coord]
        if crate_letter == ' ':
            break
        orig_stacks[stack_i].append(crate_letter)
move_line_index = stack_numbering_index + 2

stacks = copy.deepcopy(orig_stacks)
for command_line in input_lines[move_line_index:]:
    amount, source_i, target_i = [int(x) for x in re.fullmatch(r"move (\d+) from (\d+) to (\d+)", command_line).groups()]
    source = stacks[source_i]
    target = stacks[target_i]
    # move 1 crate at a time
    while amount > 0:
        amount -= 1
        crate = source.pop()
        target.append(crate)

print(''.join(stack[-1] for stack in stacks[1:]))  # VJSFHWGFT

stacks = copy.deepcopy(orig_stacks)
for command_line in input_lines[move_line_index:]:
    amount, source_i, target_i = [int(x) for x in re.fullmatch(r"move (\d+) from (\d+) to (\d+)", command_line).groups()]
    source = stacks[source_i]
    target = stacks[target_i]
    # move all those crates at once
    crates_moved = source[len(source) - amount:]
    del source[len(source) - amount:]
    target = target.extend(crates_moved)

print(''.join(stack[-1] for stack in stacks[1:]))  #


