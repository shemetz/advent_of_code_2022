"""
brazenly copied and edited the solution from here:
https://github.com/eunomicZenith/advent_of_code_2022/blob/master/day16.py

I don't feel bad about it because I already solved this day once (in a terribly bad way) and later helped with the above
"""

import dataclasses
import functools
import itertools
import re
import time
from typing import List, Dict, Tuple, FrozenSet

with open('day16.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

ValveName = str
TunnelDuration = int
FlowRate = int

STARTING_VALVE_NAME = 'AA'

all_valves: Dict[ValveName, 'Valve'] = dict()


@dataclasses.dataclass
class Valve:
    name: ValveName
    flow_rate: FlowRate
    neighbors: List[Tuple[ValveName, TunnelDuration]]
    super_distances: Dict[ValveName, TunnelDuration]

    def superconnect_through_bfs(self):
        distances = {self.name: 0}
        num_of_valves = len(all_valves)
        searching_list = [self.name]
        d = 0
        while len(distances) != num_of_valves:
            d += 1
            next_to_search = []
            for valve_to_search in searching_list:
                for valve_neighbor, vn_dist in all_valves[valve_to_search].neighbors:
                    if valve_neighbor not in distances:
                        distances[valve_neighbor] = d
                        next_to_search.append(valve_neighbor)
            searching_list = next_to_search
        self.super_distances = distances


for line in input_lines:
    parsed = re.fullmatch(r"Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)", line).groups()
    valve_name, flow_rate_s, exits_s = parsed
    flow_rate = int(flow_rate_s)
    neighbor_names = exits_s.split(', ')
    neighbors = [(nn, 1) for nn in neighbor_names]
    all_valves[valve_name] = Valve(name=valve_name, flow_rate=flow_rate, neighbors=neighbors, super_distances={})
# figure out the shortest distance from any valve to all others using BFS
for v in all_valves.values():
    v.superconnect_through_bfs()
# finding the valves that have nonzero flow and are thus actually useful
useful_valves = frozenset([v.name for v in all_valves.values() if v.flow_rate > 0])


@functools.cache
def calc_pressure_gain(opened_valve_name, time_left):
    return all_valves[opened_valve_name].flow_rate * time_left


@functools.cache
def dfs_find_best_value(valve_names_set: FrozenSet, time_left: int, starting_valve_name: ValveName):
    # in case we've run out of valves (common in part 2)
    if not valve_names_set:
        return 0
    starting_valve = all_valves[starting_valve_name]
    best_pressure = 0
    for next_valve_name in valve_names_set:
        # time after moving from starting valve to this valve and also turning this valve on
        time_left_after_move = time_left - starting_valve.super_distances[next_valve_name] - 1
        if time_left_after_move <= 0:
            continue
        # make the set of remaining valves, and feed it to dfs recursively
        valves_after_next = valve_names_set.difference({next_valve_name})
        next_layer_pressure = dfs_find_best_value(valves_after_next, time_left_after_move, next_valve_name)
        possible_pressure = next_layer_pressure + calc_pressure_gain(next_valve_name, time_left_after_move)
        # check if the new pressure beats the record
        best_pressure = max(best_pressure, possible_pressure)
    return best_pressure


def part_1_search():
    time_available = 30
    return dfs_find_best_value(useful_valves, time_available, STARTING_VALVE_NAME)


def split_search():
    time_available = 26
    best_pressure = 0
    # First we split 1|14, then 2|13, etc. until we reach 7|8. Anything past that is redundant
    for size in range(1, len(useful_valves) // 2 + 1):
        for comb_1_tuple in itertools.combinations(useful_valves, size):
            # part1 and part2 are the set of valves split in two, each of them its own frozenset
            part1 = frozenset(comb_1_tuple)
            part2 = useful_valves.difference(part1)
            # calculate pressures for each of those
            part_1_pressure = dfs_find_best_value(part1, time_available, STARTING_VALVE_NAME)
            part_2_pressure = dfs_find_best_value(part2, time_available, STARTING_VALVE_NAME)
            combined_total_pressure = part_1_pressure + part_2_pressure
            # check if their combined pressure beats the record
            best_pressure = max(best_pressure, combined_total_pressure)
    return best_pressure


t1 = time.time()
print(f'Best possible pressure alone: {part_1_search()}')  # 1584
print(f'Best possible pressure with an elephant friend: {split_search()}')  # 2052
t2 = time.time()
print(f"Took {round(t2 - t1)}s")
