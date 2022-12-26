import functools
import math
import timeit
from typing import List

SNAFU_DIGIT_VALUES = {
    "2": +2,
    "1": +1,
    "0": +0,
    "-": -1,
    "=": -2,
}

SNAFU_DIGITS_FROM_VALUES = {
    +2: "2",
    +1: "1",
    +0: "0",
    -1: "-",
    -2: "=",
}


def v1_snafu_to_decimal(snafu: str) -> int:
    # converting snafu to decimal, basically by the definition of how bases work
    rising_sum = 0
    for i in range(len(snafu)):
        # going right-to-left (small digits to big digits)
        i_from_right = len(snafu) - i - 1
        digit_value = SNAFU_DIGIT_VALUES[snafu[i_from_right]]
        rising_sum += int(math.pow(5, i)) * digit_value
    return rising_sum


def v1_decimal_to_snafu(decimal: int) -> str:
    # converting basically by the standard method, each loop dividing and adding remainder.
    # (small twist because digits can be negative)
    built_up_str_as_reversed_list = []
    while decimal > 0:
        mod = decimal % 5
        if mod >= 3:
            mod -= 5  # mod now between -2 and +2
            decimal += 5  # next digit will have +1
        snafu_digit = SNAFU_DIGITS_FROM_VALUES[mod]
        built_up_str_as_reversed_list.append(snafu_digit)
        decimal //= 5  # divide by 5 without remainder
    return "".join(reversed(built_up_str_as_reversed_list))


def v1(input_lines):
    """convert to decimals, sum up, convert back"""
    return v1_decimal_to_snafu(sum(v1_snafu_to_decimal(s) for s in input_lines))


def v2_sum_up_snafus_reversed(snafu_sum_reversed: list, next_snafu_reversed: list):
    """will fill the contents of snafu_sum_reversed with the summation total, expanding it if necessary"""
    # increase length of summation list to fit this operation including possible carry-overs
    next_snafu_reversed.extend([0, 0, 0])
    carry_over = 0
    for i in range(len(next_snafu_reversed)):
        total = snafu_sum_reversed[i] + next_snafu_reversed[i] + carry_over
        carry_over = (total + 2) // 5
        snafu_sum_reversed[i] = total - carry_over * 5


def v2(input_lines):
    snafus_reversed = [list(SNAFU_DIGIT_VALUES[d] for d in reversed(s)) for s in input_lines]
    length_of_longest_snafu = max(len(s) for s in input_lines)
    # adding a bunch of extra space up front to ongoing_sum_reversed so that we never need to extend it
    length_of_counters_list = length_of_longest_snafu + len(input_lines) // 5
    ongoing_sum_reversed = [0] * length_of_counters_list
    for s_reversed in snafus_reversed:
        v2_sum_up_snafus_reversed(ongoing_sum_reversed, s_reversed)
    sum_in_snafu_with_extra_0s = "".join(SNAFU_DIGITS_FROM_VALUES[d] for d in reversed(ongoing_sum_reversed))
    sum_in_snafu = sum_in_snafu_with_extra_0s.lstrip("0")
    return sum_in_snafu


SNAFU_DIGIT_INDICES = {
    "2": 3,
    "1": 2,
    "0": None,
    "-": 1,
    "=": 0,
}


def v3(input_lines):
    """keep in base snafu throughout (almost), add counters of digits"""
    length_of_longest_snafu = max(len(s) for s in input_lines)
    # adding a bunch of extra space up front to counters_by_digits so that we never need to extend it
    length_of_counters_list = length_of_longest_snafu + len(input_lines) // 5
    counters_by_digit: List[List[int]] = [[0, 0, 0, 0] for _ in range(length_of_counters_list)]
    for snafu_str in input_lines:
        s_reversed = list(SNAFU_DIGIT_INDICES[d] for d in reversed(snafu_str))
        for digit_i in range(len(s_reversed)):
            c_i = s_reversed[digit_i]
            if c_i is not None:  # 0s are ignored
                counters_by_digit[digit_i][c_i] += 1
    final_digits_reversed_list = []
    for digit_i in range(length_of_counters_list - 1):
        min2s, min1s, pls1s, pls2s = counters_by_digit[digit_i]
        # convert 2N x +1 into N x +2
        pls2s, pls1s = pls2s + pls1s // 2, pls1s % 2
        # convert 2N x -1 into N x -2
        min2s, min1s = min2s + min1s // 2, min1s % 2
        # balance out negatives and positives
        minimum_of_2s_counters = min(min2s, pls2s)
        min2s, pls2s = min2s - minimum_of_2s_counters, pls2s - minimum_of_2s_counters
        minimum_of_1s_counters = min(min1s, pls1s)
        min1s, pls1s = min1s - minimum_of_1s_counters, pls1s - minimum_of_1s_counters
        # left over with only +2s or -2s, plus one potential +1 or -1
        # convert every five 2s into a single 2s of next digit
        counters_by_digit[digit_i + 1][3] += pls2s // 5
        pls2s = pls2s % 5
        counters_by_digit[digit_i + 1][0] += min2s // 5
        min2s = min2s % 5
        # add up remaining, actual conversion to decimal happens here.  -9 to +9
        remaining_total = -2 * min2s + -1 * min1s + 1 * pls1s + 2 * pls2s
        while remaining_total > 2:
            counters_by_digit[digit_i + 1][2] += 1
            remaining_total -= 5
        while remaining_total < -2:
            counters_by_digit[digit_i + 1][1] += 1
            remaining_total += 5
        final_digit_here = SNAFU_DIGITS_FROM_VALUES[remaining_total]
        final_digits_reversed_list.append(final_digit_here)
    sum_in_snafu_with_extra_0s = "".join(d for d in reversed(final_digits_reversed_list))
    sum_in_snafu = sum_in_snafu_with_extra_0s.lstrip("0")
    return sum_in_snafu


def v4(input_lines):
    """add counters of digits, then convert to decimal and back at the end"""
    length_of_longest_snafu = max(len(s) for s in input_lines)
    # adding a bunch of extra space up front to counters_by_digits so that we never need to extend it
    length_of_counters_list = length_of_longest_snafu + len(input_lines) // 3
    counters_by_digit: List[List[int]] = [[0, 0, 0, 0] for _ in range(length_of_counters_list)]
    for snafu_str in input_lines:
        s_reversed = list(SNAFU_DIGIT_INDICES[d] for d in reversed(snafu_str))
        for digit_i in range(len(s_reversed)):
            c_i = s_reversed[digit_i]
            if c_i is not None:  # 0s are ignored
                counters_by_digit[digit_i][c_i] += 1
    final_sum_decimal = sum(
        math.pow(5, i) *
        (-2 * c[0] - 1 * c[1] + 1 * c[2] + 2 * c[3])
        for i, c in enumerate(counters_by_digit))
    sum_in_snafu = v1_decimal_to_snafu(final_sum_decimal)
    return sum_in_snafu


RUN_COUNT = 1000


def main():
    with open('day25.txt') as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    print(f"V1: {v1(input_lines)}")
    print(f"V2: {v2(input_lines)}")
    print(f"V3: {v3(input_lines)}")
    print(f"V4: {v4(input_lines)}")
    print(f"V1 took: {timeit.timeit(lambda: v1(input_lines), number=RUN_COUNT) / RUN_COUNT}s")
    print(f"V2 took: {timeit.timeit(lambda: v2(input_lines), number=RUN_COUNT) / RUN_COUNT}s")
    print(f"V3 took: {timeit.timeit(lambda: v3(input_lines), number=RUN_COUNT) / RUN_COUNT}s")
    print(f"V4 took: {timeit.timeit(lambda: v4(input_lines), number=RUN_COUNT) / RUN_COUNT}s")


if __name__ == '__main__':
    main()
