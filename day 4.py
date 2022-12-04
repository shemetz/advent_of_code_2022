with open('day4.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

count = 0
for line in input_lines:
    half_1, half_2 = line.split(',')
    e1s, e1e = [int(x) for x in half_1.split('-')]
    e2s, e2e = [int(x) for x in half_2.split('-')]
    if e1s <= e2s <= e2e <= e1e or e2s <= e1s <= e1e <= e2e:
        # e1 fully contains e2 or e2 fully contains e1
        count += 1

print(count)  # 477

count = 0
for line in input_lines:
    half_1, half_2 = line.split(',')
    e1s, e1e = [int(x) for x in half_1.split('-')]
    e2s, e2e = [int(x) for x in half_2.split('-')]
    if not (e2e < e1s or e1e < e2s):
        # e1 fully contains e2
        count += 1

print(count)  # 830
