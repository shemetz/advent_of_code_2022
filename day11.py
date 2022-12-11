import dataclasses
import math
import re
from typing import List

with open('day11.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


@dataclasses.dataclass
class Monkey:
    starting_items: List[int]
    operation: str
    test_divisible_by: int
    if_true_monkey_index: int
    if_false_monkey_index: int
    inspection_count: int
    inventory: List[int]

    def initialize(self):
        self.inspection_count = 0
        self.inventory = self.starting_items.copy()

    def simulate_turn(self, monkeys: List['Monkey'], divide_by_x: int, modulo_x: int):
        self.inspection_count += len(self.inventory)
        while self.inventory:
            # grab item
            item = self.inventory.pop(0)
            # do operation
            if 'old + ' in self.operation:
                item = item + int(self.operation.split(' + ')[1])
            elif 'old * old' in self.operation:
                item = item * item
            elif 'old * ' in self.operation:
                item = item * int(self.operation.split(' * ')[1])
            else:
                print(f"UNEXPECTED OPERATION!", self.operation)
            # identical step for all monkeys
            if divide_by_x != 0:
                item = item // divide_by_x
            if modulo_x != 0:
                item = item % modulo_x
            # test
            if item % self.test_divisible_by == 0:
                # throw to monkey A
                monkeys[self.if_true_monkey_index].inventory.append(item)
            else:
                # throw to monkey B
                monkeys[self.if_false_monkey_index].inventory.append(item)

monkeys: List[Monkey] = []


def setup():
    monkeys.clear()
    for i in range(len(input_lines) // 7 + 1):
        monkey_lines = [line.strip() for line in input_lines[i * 7:i * 7 + 6]]
        monkey_index = [int(x) for x in re.fullmatch(r"Monkey (\d+):", monkey_lines[0]).groups()]  # unused
        starting_items = [int(x) for x in monkey_lines[1][len("Starting items: "):].split(', ')]
        operation = monkey_lines[2][len("Operation: new = "):]
        test_divisible_by = int(monkey_lines[3][len("Test: divisible by "):])
        if_true_monkey_index = int(monkey_lines[4][len("If true: throw to monkey "):])
        if_false_monkey_index = int(monkey_lines[5][len("If false: throw to monkey "):])
        monkey = Monkey(starting_items.copy(), operation, test_divisible_by, if_true_monkey_index, if_false_monkey_index, 0, starting_items.copy())
        monkey.initialize()
        monkeys.append(monkey)


def solve_part_1():
    setup()
    TOTAL_ROUND_COUNT = 20
    for round_i in range(TOTAL_ROUND_COUNT):
        for monkey in monkeys:
            monkey.simulate_turn(monkeys, 3, 0)
    monkey_inspection_counts = [m.inspection_count for m in monkeys]
    monkey_inspection_counts.sort(reverse=True)
    monkey_business = monkey_inspection_counts[0] * monkey_inspection_counts[1]
    print(monkey_business)  # 58794


solve_part_1()


def solve_part_2():
    setup()
    TOTAL_ROUND_COUNT = 10_000
    product_of_primes = math.prod(m.test_divisible_by for m in monkeys)
    print(f'(always mods by {product_of_primes})')
    for round_i in range(TOTAL_ROUND_COUNT):
        for monkey in monkeys:
            monkey.simulate_turn(monkeys, 0, product_of_primes)
    monkey_inspection_counts = [m.inspection_count for m in monkeys]
    monkey_inspection_counts.sort(reverse=True)
    monkey_business = monkey_inspection_counts[0] * monkey_inspection_counts[1]
    print(monkey_business)  #


solve_part_2()