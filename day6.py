from collections import defaultdict

with open('day6.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]
big_line = input_lines[0]


def solve(window_size: int):
    actual_window_size = window_size - 1
    chars_in_window = defaultdict(lambda: 0)  # will always contain actual_window_size letters
    for i in range(actual_window_size):
        chars_in_window[big_line[i]] += 1
    for i in range(len(big_line) - window_size):
        left_i = i
        right_i = i + actual_window_size
        if chars_in_window[big_line[right_i]] == 0:
            if all(value <= 1 for value in chars_in_window.values()):
                # we're done
                print(right_i + 1)  # 1343
                break
        chars_in_window[big_line[left_i]] -= 1
        chars_in_window[big_line[right_i]] += 1


solve(4)
solve(14)
