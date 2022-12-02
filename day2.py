with open('day2.txt') as input_file:
    input_lines = input_file.readlines()

MATCHUP_SCORES_1 = {
    ('A', 'X'): 3 + 1,
    ('A', 'Y'): 6 + 2,
    ('A', 'Z'): 0 + 3,
    ('B', 'X'): 0 + 1,
    ('B', 'Y'): 3 + 2,
    ('B', 'Z'): 6 + 3,
    ('C', 'X'): 6 + 1,
    ('C', 'Y'): 0 + 2,
    ('C', 'Z'): 3 + 3,
}


def calc_matchup_score_1(enemy, me):
    return MATCHUP_SCORES_1[(enemy, me)]


total_score = 0
for line in input_lines:
    enemy, me = line.rstrip('\n').split(' ')
    total_score += calc_matchup_score_1(enemy, me)

print(total_score)  # 9651

MATCHUP_SCORES_2 = {
    ('A', 'X'): 0 + 3,
    ('A', 'Y'): 3 + 1,
    ('A', 'Z'): 6 + 2,
    ('B', 'X'): 0 + 1,
    ('B', 'Y'): 3 + 2,
    ('B', 'Z'): 6 + 3,
    ('C', 'X'): 0 + 2,
    ('C', 'Y'): 3 + 3,
    ('C', 'Z'): 6 + 1,
}


def calc_matchup_score_2(enemy, outcome):
    return MATCHUP_SCORES_2[(enemy, outcome)]


total_score = 0
for line in input_lines:
    enemy, outcome = line.rstrip('\n').split(' ')
    total_score += calc_matchup_score_2(enemy, outcome)

print(total_score)  # 10560
