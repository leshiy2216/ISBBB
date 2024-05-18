import json
import math

from scipy.special import gammaincc

PI_VALUES = [0.2148, 0.3672, 0.2305, 0.1875]


# first test
def frequency_test(sequence):
    n = len(sequence)
    s_obs = sum(1 if bit == '1' else -1 for bit in sequence)
    s_obs = abs(s_obs) / math.sqrt(n)
    p_value = gammaincc(n/2, s_obs**2 / 2)
    return p_value


# second test
def block_frequency_test(sequence, block_size=8):
    n = len(sequence)
    num_blocks = n // block_size
    proportions = []

    for i in range(num_blocks):
        block = sequence[i * block_size:(i + 1) * block_size]
        ones_count = block.count('1')
        pi = ones_count / block_size
        proportions.append(pi)
    
    chi_squared = 4 * block_size * sum((pi - 0.5)**2 for pi in proportions)
    p_value = gammaincc(num_blocks / 2, chi_squared / 2)
    return p_value


# third test
def longest_run_of_ones_test(sequence):
    n = len(sequence)
    max_run = 0
    cur_run = 0
    for bit in sequence:
        if bit == '1':
            cur_run += 1
            max_run = max(max_run, cur_run)
        else:
            cur_run = 0
    if max_run <= 25:
        v = 0
        for k in range(max_run + 1):
            v += (PI_VALUES[k] * (n - k))
        p_value = math.erfc(abs(v - 0.5) / (math.sqrt(2) * 0.5))
    else:
        p_value = 0.0
    return p_value


def read_bit_sequences_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data