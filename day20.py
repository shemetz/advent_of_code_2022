with open('day20.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

encrypted_original = [(i, int(n_str)) for i, n_str in enumerate(input_lines)]
length = len(encrypted_original)


def mix(original, mixed_copy):
    for num_pair in original:
        _, num = num_pair
        curr_i = mixed_copy.index(num_pair)
        next_i = (curr_i + num) % (length - 1)
        pair = mixed_copy.pop(curr_i)
        mixed_copy.insert(next_i, pair)


def get_grove_coords_sum(mixed_copy):
    val_0_pair = next(p for p in mixed_copy if p[1] == 0)
    val_0_index = mixed_copy.index(val_0_pair)
    grove_coords_indices = [(val_0_index + 1000 * i) % length for i in range(1, 3 + 1)]
    grove_coords = [mixed_copy[c_i][1] for c_i in grove_coords_indices]
    return sum(grove_coords)


mixed_once = encrypted_original.copy()
mix(encrypted_original, mixed_once)
solution_1 = get_grove_coords_sum(mixed_once)
print(f"Part 1 solution: {solution_1}")  # 19070

DECRYPTION_KEY = 811589153
actual_enc_orig = [(orig_i, 811589153 * orig_v) for orig_i, orig_v in encrypted_original]
mixed_decice = actual_enc_orig.copy()
for _ in range(10):
    mix(actual_enc_orig, mixed_decice)
solution_2 = get_grove_coords_sum(mixed_decice)
print(f"Part 2 solution: {solution_2}")  # 14773357352059
