import json

from typing import List, Dict


def read_bit_sequences_from_json(filename: str) -> Dict[str, str]:
    """
    Read bit sequences from a JSON file.

    Args:
        filename (str): The name of the JSON file.

    Returns:
        Dict[str, str]: A dictionary where keys are sequence names and values are bit sequences.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        raise
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{filename}' содержит некорректный JSON.")
        raise
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        raise