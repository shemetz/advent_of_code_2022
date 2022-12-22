import dataclasses
import operator as op_module
from typing import Optional, Dict
from magnificent_tree_print import magnificent_tree_print

with open('day21.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

OPERATOR_CHARS_TO_FUNCTIONS = {
    '+': op_module.add,
    '-': op_module.sub,
    '*': op_module.mul,
    '/': op_module.ifloordiv,
}


@dataclasses.dataclass
class Monkey:
    name: str
    listener: Optional["Monkey"] = None
    left: Optional["Monkey"] = None
    right: Optional["Monkey"] = None
    value: Optional[int] = None
    operator: Optional[str] = None  # Union["+", "-", "*", "/", None]

    def __eq__(self, other: "Monkey"):
        return self.name == other.name

    def __repr__(self):
        if self.operator is None:
            return f"🐵 {self.name} {self.value}"
        else:
            return f"🐵 {self.name} {self.value} = {self.left.name} {self.operator} {self.right.name}"

    def __str__(self):
        if self.name == NAME_OF_HUMAN:
            return f"{self.name}🧑{self.value}"
        return f"{self.name}🐵{self.value}"

    def listen_to_monkeys(self):
        did_hear_both = self.left.value is not None and self.right.value is not None
        if did_hear_both:
            self.value = OPERATOR_CHARS_TO_FUNCTIONS[self.operator](self.left.value, self.right.value)
            if self.listener is not None:
                self.listener.listen_to_monkeys()


monkeys_by_name: Dict[str, Monkey] = {}
NAME_OF_ROOT = 'root'
NAME_OF_HUMAN = 'humn'
UNKNOWN = '???'


# listeners_by_shouters: Dict[str, str] = {}
# shouters_by_listeners: Dict[str, str] = {}


def solve():
    for line in input_lines:
        monkey_name, rest = line.split(': ')
        if ' ' not in rest:  # immediate value monkey
            parsed_value = int(rest)
            if monkey_name not in monkeys_by_name:
                monkeys_by_name[monkey_name] = Monkey(name=monkey_name, value=parsed_value)
            else:  # listener created it before we found it
                me_monkey = monkeys_by_name[monkey_name]
                me_monkey.value = parsed_value
                listener = me_monkey.listener
                listener.listen_to_monkeys()
        else:  # operation monkey
            left_name, operator, right_name = rest.split(' ')
            if monkey_name not in monkeys_by_name:
                me_monkey = Monkey(name=monkey_name, operator=operator)
                monkeys_by_name[monkey_name] = me_monkey
            else:
                me_monkey = monkeys_by_name[monkey_name]
                me_monkey.operator = operator
            if left_name not in monkeys_by_name:
                left_monkey = Monkey(name=left_name, listener=me_monkey)
                monkeys_by_name[left_name] = left_monkey
            else:
                left_monkey = monkeys_by_name[left_name]
                left_monkey.listener = me_monkey
            if right_name not in monkeys_by_name:
                right_monkey = Monkey(name=right_name, listener=me_monkey)
                monkeys_by_name[right_name] = right_monkey
            else:
                right_monkey = monkeys_by_name[right_name]
                right_monkey.listener = me_monkey
            me_monkey.left = left_monkey
            me_monkey.right = right_monkey
            me_monkey.listen_to_monkeys()
    root = monkeys_by_name[NAME_OF_ROOT]
    print("Part 1 solution:", root.value)  # 160274622817992

    # part 2
    root.operator = '='
    root.value = '—'
    humn = monkeys_by_name[NAME_OF_HUMAN]
    # mark the way up the tree to the root
    monkey_goes_up = humn
    while monkey_goes_up is not root:
        monkey_goes_up.value = UNKNOWN  # 🙉
        monkey_goes_up = monkey_goes_up.listener
    # and now we start going down in that direction
    monkey_goes_down = root.right if root.right.value == UNKNOWN else root.left
    monkey_goes_down.value = root.left.value if root.right.value == UNKNOWN else root.right.value
    while monkey_goes_down is not humn:
        # in each loop, we have the monkey's value and its non-human-side value and its operation;  we use those
        # to calculate what the human-side child's value needs to be, and then continue downwards to that child
        human_child_is_right = monkey_goes_down.right.value == UNKNOWN
        human_side_child = monkey_goes_down.right if human_child_is_right else monkey_goes_down.left
        valued_child = monkey_goes_down.left if human_child_is_right else monkey_goes_down.right
        other_child_value = valued_child.value
        listener_value = monkey_goes_down.value
        if monkey_goes_down.operator == '+':
            human_side_child.value = listener_value - other_child_value
        if monkey_goes_down.operator == '-':
            human_side_child.value = (other_child_value - listener_value) if human_child_is_right else (
                        listener_value + other_child_value)
        if monkey_goes_down.operator == '*':
            human_side_child.value = listener_value // other_child_value
        if monkey_goes_down.operator == '/':
            human_side_child.value = (other_child_value // listener_value) if human_child_is_right else (
                        listener_value * other_child_value)
        monkey_goes_down = human_side_child
    print("Part 2 solution:", humn.value)  # 3087390115721
    magnificent_tree_print(root, shorten_per_piece_width_by=4)


solve()
