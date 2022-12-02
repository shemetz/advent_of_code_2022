with open('day1.txt') as input_file:
    input_lines = input_file.readlines()

input_lines.append('\n')
current_counter = 0
best_found = 0
for line in input_lines:
    if line.rstrip('\n') == '':
        if current_counter >= best_found:
            best_found = current_counter
        current_counter = 0
        continue
    current_counter += int(line.rstrip('\n'))

print(best_found)  # 67016

# trying to do it in a single pass
current_counter = 0
bests_found = [0, 0, 0]
for line in input_lines:
    if line.rstrip('\n') == '':
        for i in reversed(range(len(bests_found))):
            if current_counter >= bests_found[i]:
                bests_found = bests_found[1:i+1] + [current_counter] + bests_found[i+1:]
                break
        current_counter = 0
        continue
    current_counter += int(line.rstrip('\n'))

print(sum(bests_found))  # 200116
