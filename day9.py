import dataclasses
from typing import Set

with open('day9.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


Delta = Point

DIRECTIONS_TO_COORDS = {
    'R': Delta(+1, 0),
    'L': Delta(-1, 0),
    'U': Delta(0, +1),
    'D': Delta(0, -1),
}


class RopeSimulator:
    def __init__(self):
        self.head = Point(0, 0)
        self.tail = Point(0, 0)
        self.visited_by_tail: Set[Point] = {Point(0, 0)}

    def simulate_step(self, direction: str):
        change = DIRECTIONS_TO_COORDS[direction]
        self.head = Point(self.head.x + change.x, self.head.y + change.y)
        # move tail logically
        delta_x = self.head.x - self.tail.x
        delta_y = self.head.y - self.tail.y
        abs_delta = abs(delta_x) + abs(delta_y)
        if abs_delta <= 1:
            return
        if abs_delta > 2:
            # force diagonal move with an ugly ugly hack to trick the rounding
            delta_x *= 1.1
            delta_y *= 1.1
        self.tail = Point(self.tail.x + round(delta_x / 2), self.tail.y + round(delta_y / 2))

    def solve_part_a(self):
        for line in input_lines:
            direction, dist = line.split(' ')
            distance = int(dist)
            # print(line)
            for _ in range(distance):
                self.simulate_step(direction)
                self.visited_by_tail.add(self.tail)
                # print(self.tail)
        print(len(self.visited_by_tail))  # 6486


RopeSimulator().solve_part_a()


class RopeSimulator2:
    def __init__(self, rope_length: int):
        self.rope = [Point(0, 0) for _ in range(rope_length)]
        self.visited_by_tail: Set[Point] = {Point(0, 0)}

    def simulate_entire_step(self, direction: str):
        change = DIRECTIONS_TO_COORDS[direction]
        head = self.rope[0]
        head = Point(head.x + change.x, head.y + change.y)
        self.rope[0] = head
        for i in range(1, len(self.rope)):
            self.simulate_knot_step(i)

    def simulate_knot_step(self, knot_i: int):
        leader = self.rope[knot_i - 1]
        follower = self.rope[knot_i]
        # move follower based on leader which already moved
        delta_x = leader.x - follower.x
        delta_y = leader.y - follower.y
        abs_delta = abs(delta_x) + abs(delta_y)
        if abs_delta <= 1:
            return
        if abs_delta > 2:
            # force diagonal move with an ugly ugly hack to trick the rounding
            delta_x *= 1.1
            delta_y *= 1.1
        follower = Point(follower.x + round(delta_x / 2), follower.y + round(delta_y / 2))
        self.rope[knot_i] = follower

    def solve_part_2(self):
        for line in input_lines:
            direction, dist = line.split(' ')
            distance = int(dist)
            # print(line)
            for _ in range(distance):
                self.simulate_entire_step(direction)
                tail = self.rope[-1]
                self.visited_by_tail.add(tail)
                # print(self.tail)
        print(len(self.visited_by_tail))  # 2678


RopeSimulator2(10).solve_part_2()
