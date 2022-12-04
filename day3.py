with open('day3.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


def calc_priority(char: str):
    ord_num = ord(char)
    if ord('a') <= ord_num <= ord('z'):
        return ord_num - ord('a') + 1
    if ord('A') <= ord_num <= ord('Z'):
        return ord_num - ord('A') + 1 + 26
    raise ValueError(f'unexpected char {char}')


priorities_sum = 0
for line in input_lines:
    half = len(line) // 2
    c1, c2 = line[:half], line[half:]
    s1, s2 = set(c1), set(c2)
    inters = s1.intersection(s2)
    one_shared_item = inters.pop()
    priorities_sum += calc_priority(one_shared_item)

print(priorities_sum)  # 8185

priorities_sum = 0
for i in range(0, len(input_lines), 3):
    e1, e2, e3 = input_lines[i: i + 3]
    s1, s2, s3 = set(e1), set(e2), set(e3)
    inters = s1.intersection(s2).intersection(s3)
    one_shared_item = inters.pop()
    priorities_sum += calc_priority(one_shared_item)

print(priorities_sum)  # 2817
