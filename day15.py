import re
from typing import Tuple, List, Set

with open('day15.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

Range = Tuple[int, int]  # left, right (not including right)

TARGET_ROW = 2_000_000
# TARGET_ROW = 10

covered_ranges: List[Range] = []
beacons_on_row: Set[int] = set()
for line in input_lines:
    parsed = re.fullmatch(r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)", line).groups()
    s_x, s_y, b_x, b_y = [int(n) for n in parsed]
    sensor_range = abs(s_x - b_x) + abs(s_y - b_y)
    delta_y = abs(s_y - TARGET_ROW)
    remaining_delta_x = sensor_range - delta_y
    if remaining_delta_x >= 0:
        covered_ranges.append((s_x - remaining_delta_x, s_x + remaining_delta_x + 1))
    if b_y == TARGET_ROW:
        beacons_on_row.add(b_x)

ranges_sorted_by_start = sorted(covered_ranges)
ranges_no_intersection = [ranges_sorted_by_start[0]]
for range_r in ranges_sorted_by_start:
    prev_range = ranges_no_intersection[-1]
    if range_r[0] <= prev_range[1]:
        # if intersection, combine and replace latest
        new_range = (prev_range[0], max(range_r[1], prev_range[1]))
        ranges_no_intersection[-1] = new_range
    else:
        # just add
        ranges_no_intersection.append(range_r)

total_covered_area = sum(r[1] - r[0] for r in ranges_no_intersection) - len(beacons_on_row)
print('Part 1 answer:', total_covered_area)  # 4793062

MIN_X = 0
MAX_X = 4_000_000
# MAX_X = 20
MIN_Y = 0
MAX_Y = 4_000_000
# MAX_Y = 20

parsed_sensors = []
for line in input_lines:
    parsed = re.fullmatch(r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)", line).groups()
    s_x, s_y, b_x, b_y = [int(n) for n in parsed]
    parsed_sensors.append((s_x, s_y, b_x, b_y))


for y in range(MIN_Y, MAX_Y + 1):
    target_row = y
    covered_ranges: List[Range] = []
    for s_x, s_y, b_x, b_y in parsed_sensors:
        sensor_range = abs(s_x - b_x) + abs(s_y - b_y)
        delta_y = abs(s_y - target_row)
        remaining_delta_x = sensor_range - delta_y
        if remaining_delta_x >= 0:
            covered_ranges.append((s_x - remaining_delta_x, s_x + remaining_delta_x + 1))

    ranges_sorted_by_start = sorted(covered_ranges)
    ranges_no_intersection = [ranges_sorted_by_start[0]]
    for range_r in ranges_sorted_by_start:
        prev_range = ranges_no_intersection[-1]
        if range_r[0] <= prev_range[1]:
            # if intersection, combine and replace latest
            new_range = (prev_range[0], max(range_r[1], prev_range[1]))
            ranges_no_intersection[-1] = new_range
        else:
            # just add
            ranges_no_intersection.append(range_r)
    ranges_no_intersection = [(max(MIN_X, r[0]), min(MAX_X, r[1])) for r in ranges_no_intersection]
    total_covered_area = sum(r[1] - r[0] for r in ranges_no_intersection)
    if total_covered_area == MAX_X - MIN_X:
        continue
    # FOUND IT!
    print('Part 2 coords:', ranges_no_intersection[0][1], y)
    print('Part 2 solution:', ranges_no_intersection[0][1] * 4000000 + y)  # 10826395253551
    break

#  TODO - consider cool solution of only looking at points near near-intersections of edges.  currently p2 takes so long
