import dataclasses
import re
from typing import List, Dict, Tuple, Set

with open('day16.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


ValveName = str
TunnelDuration = int
FlowRate = int


@dataclasses.dataclass
class Valve:
    name: ValveName
    flow_rate: FlowRate
    neighbors: List[Tuple[ValveName, TunnelDuration]]


valves: Dict[ValveName, Valve] = dict()
for line in input_lines:
    parsed = re.fullmatch(r"Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)", line).groups()
    valve_name, flow_rate_s, exits_s = parsed
    flow_rate = int(flow_rate_s)
    neighbor_names = exits_s.split(', ')
    neighbors = [(nn, 1) for nn in neighbor_names]
    valve = Valve(name=valve_name, flow_rate=flow_rate, neighbors=neighbors)
    valves[valve_name] = valve

# remove 0-flow-rate valves
for zero_valve_name, zero_valve in list(valves.items()):
    if zero_valve.flow_rate > 0:
        continue
    if zero_valve_name == 'AA':
        # special starter valve
        continue
    neighbors = list(zero_valve.neighbors).copy()
    for neighbor_name, td in zero_valve.neighbors:
        neighbor_neighbors = valves[neighbor_name].neighbors
        prev_tunnel_duration = -1
        for vn, td in neighbor_neighbors:
            if vn == zero_valve_name:
                prev_tunnel_duration = td
        # remove this from its neighbors
        neighbor_neighbors.remove((zero_valve_name, prev_tunnel_duration))
        # add new links with longer duration
        for neighbor_name_2, td_2 in zero_valve.neighbors:
            if neighbor_name != neighbor_name_2:
                neighbor_neighbors.append((neighbor_name_2, td_2 + prev_tunnel_duration))
    valves.pop(zero_valve_name)


# # print nicer
# for vname, v in valves.items():
#     print(vname, v.flow_rate, v.neighbors)

@dataclasses.dataclass
class Progress:
    time_left: int
    score_so_far: int
    position: ValveName
    opened_valves: Set[ValveName]

    def partial_tupled(self):
        return self.time_left, self.position, tuple(sorted(self.opened_valves))

    def __eq__(self, other):
        return other.tupled() == self.partial_tupled()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.partial_tupled())


# try solving
initial_progress = Progress(30, 0, 'AA', set())
all_current_progresses: List[Progress] = [initial_progress]

max_flow_rate = sum(v.flow_rate for v in valves.values())
best_score_so_far = 0
# for each combination of position and opened valves:
#   we keep a set of (time, score) pairs
#   later we will check them to prune other worse solutions
progresses_seen_already: Dict[tuple, Set[Tuple[int, int]]] = {initial_progress.partial_tupled(): {(0, 30)}}

while all_current_progresses:
    progress: Progress = all_current_progresses.pop()
    # prune if illegal (spent too much time)
    if progress.time_left <= 0:
        continue
    # prune if can't reach current high score.  narrow but helpful
    if best_score_so_far >= progress.score_so_far + max_flow_rate * progress.time_left:
        continue
    # prune if seen already (this or a better thing)
    tupled_prog = progress.partial_tupled()
    existing_similar_progresses = progresses_seen_already.get(tupled_prog, set())
    if any(
        progress.time_left <= tl and progress.score_so_far <= ssf
        for tl, ssf in existing_similar_progresses
    ):
        continue
    # keep track of this one
    existing_similar_progresses.add((progress.time_left, progress.score_so_far))
    progresses_seen_already[tupled_prog] = existing_similar_progresses
    # now, add all possible continuations
    sum_of_current_flow_rates = sum(valves[vn].flow_rate for vn in progress.opened_valves)
    # 1. turn on current valve
    if progress.position not in progress.opened_valves:
        new_opened_valves = progress.opened_valves.copy()
        new_opened_valves.add(progress.position)
        all_current_progresses.append(Progress(
            time_left=progress.time_left - 1,
            score_so_far=progress.score_so_far + sum_of_current_flow_rates,
            position=progress.position,
            opened_valves=new_opened_valves,
        ))
    # 2. move to neighbor
    for neighbor_name, tunnel_duration in valves[progress.position].neighbors:
        if tunnel_duration >= progress.time_left:
            # don't bother
            continue
        all_current_progresses.append(Progress(
            time_left=progress.time_left - tunnel_duration,
            score_so_far=progress.score_so_far + sum_of_current_flow_rates * tunnel_duration,
            position=neighbor_name,
            opened_valves=progress.opened_valves.copy(),
        ))
    # 3. wait in place until the end
    final_score_if_staying = progress.score_so_far + sum_of_current_flow_rates * progress.time_left
    best_score_so_far = max(best_score_so_far, final_score_if_staying)

print('Part 1:', best_score_so_far)  # 1584


# part 2: ELEPHANT

valves: Dict[ValveName, Valve] = dict()
for line in input_lines:
    parsed = re.fullmatch(r"Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)", line).groups()
    valve_name, flow_rate_s, exits_s = parsed
    flow_rate = int(flow_rate_s)
    neighbor_names = exits_s.split(', ')
    neighbors = [(nn, 1) for nn in neighbor_names]
    valve = Valve(name=valve_name, flow_rate=flow_rate, neighbors=neighbors)
    valves[valve_name] = valve


@dataclasses.dataclass
class ProgressStepByStep:
    score_so_far: int
    positions: Tuple[ValveName, ValveName]  # sorted by valve name
    opened_valves: Set[ValveName]
    leftover_sum_of_flow_rates: int

    def partial_tupled(self):
        return self.positions, tuple(sorted(self.opened_valves))

    def __eq__(self, other):
        return other.tupled() == self.partial_tupled()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.partial_tupled())


# try solving
max_flow_rate = sum(v.flow_rate for v in valves.values())
initial_progress = ProgressStepByStep(0, ('AA', 'AA'), set(), max_flow_rate)
all_current_progresses_2: List[ProgressStepByStep] = [initial_progress]

best_score_so_far = 0
# for each combination of positions and opened valves:
#   we keep a best score so far
#   later we will check it to prune other worse solutions
progresses_seen_already: Dict[tuple, int] = {}

time_left = 26
while time_left > 0:
    next_step_progresses = []
    print(f"time left: {time_left}, current best: {best_score_so_far}")
    for progress_2 in all_current_progresses_2:
        # prune if can't reach current high score.  narrow but helpful
        if best_score_so_far >= progress_2.score_so_far + progress_2.leftover_sum_of_flow_rates * time_left:
            continue
        progress_2.positions = tuple(sorted(progress_2.positions))
        # prune if seen already (this or a better thing)
        tupled_prog = progress_2.partial_tupled()
        other_score_from_same_situation = progresses_seen_already.get(tupled_prog, -1)
        if other_score_from_same_situation >= progress_2.score_so_far:
            continue
        # keep track of this one
        progresses_seen_already[tupled_prog] = progress_2.score_so_far
        best_score_so_far = max(best_score_so_far, progress_2.score_so_far)
        # now, add all possible continuations
        partial_progresses_forward = []
        pos_0, pos_1 = progress_2.positions
        # 1. turn on current valve
        if pos_0 not in progress_2.opened_valves and valves[pos_0].flow_rate > 0:
            new_opened_valves = progress_2.opened_valves.copy()
            new_opened_valves.add(pos_0)
            partial_progresses_forward.append(ProgressStepByStep(
                score_so_far=progress_2.score_so_far + valves[pos_0].flow_rate * (time_left - 1),
                positions=(pos_0, pos_1),
                opened_valves=new_opened_valves,
                leftover_sum_of_flow_rates=progress_2.leftover_sum_of_flow_rates - valves[pos_0].flow_rate,
            ))
        # 2. move to neighbor
        for neighbor_name, tunnel_duration in valves[pos_0].neighbors:
            if tunnel_duration >= time_left:
                # don't bother
                continue
            partial_progresses_forward.append(ProgressStepByStep(
                score_so_far=progress_2.score_so_far,
                positions=(neighbor_name, pos_1),
                opened_valves=progress_2.opened_valves.copy(),
                leftover_sum_of_flow_rates=progress_2.leftover_sum_of_flow_rates,
            ))
        for ppf in partial_progresses_forward:
            if pos_1 not in ppf.opened_valves and valves[pos_1].flow_rate > 0:
                new_opened_valves = ppf.opened_valves.copy()
                new_opened_valves.add(pos_1)
                next_step_progresses.append(ProgressStepByStep(
                    score_so_far=ppf.score_so_far + valves[pos_1].flow_rate * (time_left - 1),
                    positions=(ppf.positions[0], pos_1),
                    opened_valves=new_opened_valves,
                    leftover_sum_of_flow_rates=ppf.leftover_sum_of_flow_rates - valves[pos_1].flow_rate,
                ))
            # 2. move to neighbor
            for neighbor_name, tunnel_duration in valves[pos_1].neighbors:
                if tunnel_duration >= time_left:
                    # don't bother
                    continue
                next_step_progresses.append(ProgressStepByStep(
                    score_so_far=ppf.score_so_far,
                    positions=(ppf.positions[0], neighbor_name),
                    opened_valves=ppf.opened_valves.copy(),
                    leftover_sum_of_flow_rates=ppf.leftover_sum_of_flow_rates,
                ))
    time_left -= 1
    all_current_progresses_2 = next_step_progresses

print('Part 2:', best_score_so_far)  #

# TODO - DFS instead of BFS so that it doesn't take an hour to run
