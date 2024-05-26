import json
import math

from typing import List, Dict
from scipy.special import gammaincc, gammainc, erfc
from json_reader import read_bit_sequences_from_json


LENGTH_OF_BLOCK = 8
PI_I = [0.2148, 0.3672, 0.2305, 0.1875]


def frequency_test(sequence: str) -> float:
    """
    Perform the frequency test on a given bit sequence.
    
    Args:
        sequence (str): A string of bits ('0' and '1').

    Returns:
        float: The p-value of the frequency test.
    """
    try:
        N = len(sequence)
        sum = 0
        for bit in sequence:
            if bit == "0":
                sum -= 1
            else:
                sum += 1
        S_N = (1.0 / math.sqrt(N)) * abs(sum)
        P_value = erfc(S_N / math.sqrt(2))
        if P_value < 0 or P_value > 1:
            raise ValueError('P should be in range [0, 1]')
        return P_value
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise

    return P_value


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
    try:
        blocks = []
        for i in range(0, int(len(sequence) / LENGTH_OF_BLOCK)):
            blocks.append(sequence[i * LENGTH_OF_BLOCK: (i + 1) * LENGTH_OF_BLOCK])
        
        V = [0, 0, 0, 0]
        for block in blocks:
            count = 0
            max_length = 0
            for bit in block:
                if bit == "1":
                    count += 1
                    max_length = max(max_length, count)
                else:
                    count = 0
            
            if max_length <= 1:
                V[0] += 1
            elif max_length == 2:
                V[1] += 1
            elif max_length == 3:
                V[2] += 1
            elif max_length >= 4:
                V[3] += 1
        
        Xi_in_2 = 0
        for i in range(0, 4):
            Xi_in_2 += pow((V[i] - 16 * PI_I[i]), 2) / (16 * PI_I[i])
        
        P_value = gammainc(1.5, (Xi_in_2 / 2))
        
        if P_value < 0 or P_value > 1:
            raise ValueError('P should be in range [0, 1]')
        
        return P_value
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise


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