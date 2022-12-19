import dataclasses
import functools
import re
import time
from typing import Tuple, List

with open('day19.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

Ores, Clays, Obsidians, Geodes = int, int, int, int
ResourceCounts = Tuple[Ores, Clays, Obsidians, Geodes]


@dataclasses.dataclass
class Blueprint:
    id_num: int
    bot_costs: Tuple[ResourceCounts, ResourceCounts, ResourceCounts, ResourceCounts]

    def __hash__(self):
        return hash((self.id_num, self.bot_costs))


@dataclasses.dataclass
class State:
    minutes_left: int
    resources: ResourceCounts
    bot_counts: ResourceCounts

    def __hash__(self):
        return hash((self.minutes_left, self.resources, self.bot_counts))


highest_costs: ResourceCounts = (-1, -1, -1, -1)
blueprints: List[Blueprint] = []
for line in input_lines:
    numbers = [int(n) for n in re.findall(r'\d+', line)]
    blueprints.append(Blueprint(
        id_num=numbers[0],
        bot_costs=(
            (numbers[1], 0, 0, 0),
            (numbers[2], 0, 0, 0),
            (numbers[3], numbers[4], 0, 0),
            (numbers[5], 0, numbers[6], 0),
        ),
    ))
    highest_costs = (
        max(highest_costs[0], numbers[1], numbers[2], numbers[3], numbers[5]),
        max(highest_costs[1], numbers[4]),
        max(highest_costs[2], numbers[6]),
        -1,
    )

# RESOURCES = ['geode', 'obsidian', 'clay', 'ore']
RESOURCES = ['ore', 'clay', 'obsidian', 'geode']


@functools.cache
def triangle(n: int) -> int:
    """given a number n, will return 1 + 2 + 3 + ... + n-1 + n"""
    return n * (n + 1) // 2


@functools.cache
def trianglent(tn: int) -> int:
    """inverse of triangle.  will return the smallest number whose triangle is at least nt"""
    n = 0
    n_sum = 0
    while n_sum < tn:
        n += 1
        n_sum += n
    # this way we get: triangle(n-1) < tn <= triangle(n)
    return n


best_so_far: Geodes = 0
prune_metrics = [0, 0, 0, 0]


@functools.cache
def recursive_solve(blueprint: Blueprint, prev_state: State) -> Geodes:
    global best_so_far, prune_metrics
    geodes_so_far = prev_state.resources[3]
    minutes_left = prev_state.minutes_left
    # basic halting condition, technically almost never prunes anything but we'll keep it because it's simple
    if minutes_left == 0:
        prune_metrics[0] += 1
        return geodes_so_far
    # -- optimization pruning with heuristics --
    guaranteed_future_geodes = minutes_left * prev_state.bot_counts[3]
    extra_geodes_needed_to_beat_high_score = best_so_far - geodes_so_far - guaranteed_future_geodes + 1
    if extra_geodes_needed_to_beat_high_score > 0:
        # triangle math:  we need enough geodes to beat previous high score, can we make enough geode bots?
        extra_geode_bots_needed = trianglent(extra_geodes_needed_to_beat_high_score)
        if extra_geode_bots_needed > 0:
            if extra_geode_bots_needed > minutes_left - 1:
                prune_metrics[1] += 1
                return geodes_so_far
            # we need to have this much obsidian
            obsidian_cost_of_extra_geode_bots = blueprint.bot_costs[3][2]
            obsidian_so_far = prev_state.resources[2]
            minutes_left_til_geode_bot_production = minutes_left - extra_geode_bots_needed
            guar_fut_obs = minutes_left_til_geode_bot_production * prev_state.bot_counts[2]
            extra_obsidian_needed = obsidian_cost_of_extra_geode_bots - obsidian_so_far - guar_fut_obs
            if extra_obsidian_needed > 0:
                extra_obs_bots_needed = trianglent(extra_obsidian_needed)
                if extra_obs_bots_needed > minutes_left_til_geode_bot_production - 1:
                    prune_metrics[2] += 1
                    return geodes_so_far

    # we'll never need 5+ ore bots, because highest bot ore cost is 4.  (repeating for other bots is not useful)
    if prev_state.bot_counts[0] > highest_costs[0]:
        prune_metrics[3] += 1
        return geodes_so_far
    # -- recursive calculation time --
    for choice_i in range(len(RESOURCES) + 1):  # i=4 means doing nothing
        new_resources = prev_state.resources
        added = [0, 0, 0, 0]
        if choice_i != 4:
            costs = blueprint.bot_costs[choice_i]
            new_resources = tuple(prev_state.resources[i] - costs[i] for i in range(len(RESOURCES)))
            if any(r < 0 for r in new_resources):
                continue
            added[choice_i] = 1
        # noinspection PyTypeChecker
        next_state = State(
            minutes_left=minutes_left - 1,
            resources=tuple(new_resources[i] + prev_state.bot_counts[i] for i in range(len(RESOURCES))),
            bot_counts=tuple(prev_state.bot_counts[i] + added[i] for i in range(len(RESOURCES))),
        )
        choice_geodes = recursive_solve(blueprint, next_state)
        if best_so_far < choice_geodes:
            best_so_far = choice_geodes
    return best_so_far


def solve_part_1():
    starting_state = State(24, (0, 0, 0, 0), (1, 0, 0, 0))
    t1 = time.time()
    quality_level_sum = 0
    for blueprint in blueprints:
        global best_so_far
        best_so_far = 0
        blueprint_score = recursive_solve(blueprint, starting_state)
        quality_level = blueprint_score * blueprint.id_num
        quality_level_sum += quality_level
        # print(f"blueprint {blueprint.id_num} got score: {blueprint_score}")
    t2 = time.time()
    print(f'Took {round(t2 - t1)}s')
    print('Part 1 solution:', quality_level_sum)  # 1413


def solve_part_2():
    starting_state = State(32, (0, 0, 0, 0), (1, 0, 0, 0))
    t1 = time.time()
    score_prod = 1
    for blueprint in blueprints[:3]:
        global best_so_far
        best_so_far = 0
        blueprint_score = recursive_solve(blueprint, starting_state)
        quality_level = blueprint_score * blueprint.id_num
        score_prod *= quality_level
        # print(f"blueprint {blueprint.id_num} got score: {blueprint_score}")
    t2 = time.time()
    print(f'Took {round(t2 - t1)}s')
    print('Part 2 solution:', score_prod)  # 21080


# takes about 40 seconds per part!
solve_part_1()
print()
solve_part_2()

print('pruning statistics (counts and percentages, in order):')
pm_avg = sum(prune_metrics)
print([pc for pc in prune_metrics])
print([round(pc / pm_avg * 100) for pc in prune_metrics])
