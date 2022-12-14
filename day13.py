import ast

with open('day13.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


def convert(p_str):
    # yay python
    return ast.literal_eval(p_str)


def compare(p1, p2):
    """returns -1 if p1 < p2, +1 if >, and 0 if ="""
    p1_is_int = isinstance(p1, int)
    p2_is_int = isinstance(p2, int)
    if p1_is_int and p2_is_int:
        return 0 if p1 == p2 else -1 if p1 < p2 else +1
    if p1_is_int and not p2_is_int:
        p1 = [p1]
        p1_is_int = True
    if not p1_is_int and p2_is_int:
        p2 = [p2]
        p2_is_int = True
    # now they're both lists
    for j in range(max(len(p1), len(p2))):
        if j >= len(p1):
            # p1 is shorter
            return -1
        if j >= len(p2):
            # p2 is shorter
            return +1
        p1_value_at_j = p1[j]
        p2_value_at_j = p2[j]
        list_comparison = compare(p1_value_at_j, p2_value_at_j)
        if list_comparison != 0:
            return list_comparison
    return 0


packets = []
for i in range(0, len(input_lines), +3):
    packets.append((convert(input_lines[i]), convert(input_lines[i + 1])))

sum_of_good_indices = 0
for i, p1p2 in enumerate(packets):
    pair_index = i + 1
    packet_1, packet_2 = p1p2
    comparison = compare(packet_1, packet_2)
    if comparison <= 0:
        sum_of_good_indices += pair_index

print(sum_of_good_indices)  # 5684


def merge_sort(unsorted_list):
    length = len(unsorted_list)
    if length == 0:
        return []
    if length == 1:
        return unsorted_list
    pivot = unsorted_list[length // 2]
    left = []
    middle = []
    right = []
    for item in unsorted_list:
        item_pivot_comparison = compare(item, pivot)
        if item_pivot_comparison == -1:
            left.append(item)
        elif item_pivot_comparison == +1:
            right.append(item)
        else:  # item_pivot_comparison == 0
            middle.append(item)
    return merge_sort(left) + middle + merge_sort(right)


divider_packets = [
    [[2]],
    [[6]],
]

everything = [
    # given to us by AoC
    *divider_packets,
]
for pair in packets:
    everything.append(pair[0])
    everything.append(pair[1])

sorted_everything = merge_sort(everything)

index_of_divider_packet_1 = sorted_everything.index(divider_packets[0]) + 1
index_of_divider_packet_2 = sorted_everything.index(divider_packets[1]) + 1
print(index_of_divider_packet_1 * index_of_divider_packet_2)  # 22932
