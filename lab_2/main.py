import json
import math
from scipy.special import gammaincc


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