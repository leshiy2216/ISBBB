import json
import math

from typing import List, Dict
from scipy.special import gammaincc
from json_reader import read_bit_sequences_from_json


def frequency_test(sequence: str) -> float:
    """
    Perform the frequency test on a given bit sequence.
    
    Args:
        sequence (str): A string of bits ('0' and '1').

    Returns:
        float: The p-value of the frequency test.
    """
    n = len(sequence)
    s_obs = sum(1 if bit == '1' else -1 for bit in sequence)
    s_obs = abs(s_obs) / math.sqrt(n)
    p_value = gammaincc(n/2, s_obs**2 / 2)
    return p_value


def block_frequency_test(sequence: str, block_size: int = 8) -> float:
    """
    Perform the block frequency test on a given bit sequence.
    
    Args:
        sequence (str): A string of bits ('0' and '1').
        block_size (int): The size of each block. Default is 8.

    Returns:
        float: The p-value of the block frequency test.
    """
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


def longest_run_of_ones_test(sequence: str, block_size: int = 8) -> float:
    """
    Perform the longest run of ones test on a given bit sequence.
    
    Args:
        sequence (str): A string of bits ('0' and '1').
        block_size (int): The size of each block. Default is 8.

    Returns:
        float: The p-value of the longest run of ones test.
    """
    n = len(sequence)
    blocks = n // block_size

    longest_runs = []
    for i in range(blocks):
        block = sequence[i * block_size:(i + 1) * block_size]
        max_run = max(map(len, ''.join(str(x) for x in block).split('0')))
        longest_runs.append(max_run)

    pi = [0] * (block_size + 1)
    for run in longest_runs:
        if run <= block_size:
            pi[run] += 1

    pi = [x / blocks for x in pi]
    
    if block_size == 8:
        v = [0.2148, 0.3672, 0.2305, 0.1875]
        piks = [pi[1], pi[2], pi[3], sum(pi[4:])]
    elif block_size == 128:
        v = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        piks = [pi[4], pi[5], pi[6], pi[7], pi[8], sum(pi[9:])]
    elif block_size == 512:
        v = [0.1170, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        piks = [pi[10], pi[11], pi[12], pi[13], pi[14], sum(pi[15:])]

    chi_squared = sum([(obs - exp)**2 / exp for obs, exp in zip(piks, v)])

    p_value = gammaincc(len(v) / 2, chi_squared / 2)
    return p_value


def run_nist_tests(sequences: Dict[str, str]) -> None:
    """
    Run NIST tests (frequency, block frequency, longest run of ones) on sequences.
    
    Args:
        sequences (Dict[str, str]): A dictionary where keys are sequence names and values are bit sequences.
    """
    for name, sequence in sequences.items():
        print("Sequence:", name)
        print("Frequency Test p-value:", frequency_test(sequence))
        print("Block Frequency Test p-value:", block_frequency_test(sequence))
        print("Longest Run of Ones Test p-value:", longest_run_of_ones_test(sequence))
        print()


if __name__ == "__main__":
    sequences = read_bit_sequences_from_json("numbers.json")
    run_nist_tests(sequences)