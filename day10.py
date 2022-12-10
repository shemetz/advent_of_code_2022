with open('day10.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


# just simulating
def is_interesting_time(cycle_count: int):
    return (cycle_count + 20) % 40 == 0


x = 1
cycle = 1
line_i = -1
mid_operation = False
sum_of_signal_strengths = 0
while line_i < len(input_lines) - 1:
    line_i += 1
    line = input_lines[line_i]
    cycle += 1
    if line == 'noop':
        pass
    else:
        _addx, amount_str = line.split(' ')
        amount = int(amount_str)
        if not mid_operation:
            line_i -= 1  # read same line again next loop
            mid_operation = True
        else:
            x += amount
            mid_operation = False
    if is_interesting_time(cycle):
        sum_of_signal_strengths += cycle * x

print(sum_of_signal_strengths)  # 11720

x = 1
cycle = 0  # weird!  TODO figure out
line_i = -1
mid_operation = False
screen = []
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6
while line_i < len(input_lines) - 1:
    x_is_on_pixel = abs(x - cycle % SCREEN_WIDTH) <= 1
    screen.append('⬜' if x_is_on_pixel else '⬛')
    line_i += 1
    line = input_lines[line_i]
    cycle += 1
    if line == 'noop':
        pass
    else:
        _addx, amount_str = line.split(' ')
        amount = int(amount_str)
        if not mid_operation:
            line_i -= 1  # read same line again next loop
            mid_operation = True
        else:
            x += amount
            mid_operation = False

for i in range(SCREEN_HEIGHT):
    print(''.join(screen[i * SCREEN_WIDTH:(i + 1) * SCREEN_WIDTH]))  # ERCREPCJ
