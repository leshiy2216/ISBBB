import argparse
import json
from typing import Tuple


def read_settings(settings_file_path: str) -> Tuple[str, str]:
    """
    read encryption and decryption settings
    Args:
    settings_file_path: str
    """
    with open(settings_file_path, 'r', encoding='UTF-8') as settings_file:
        settings = json.load(settings_file)
    return settings.get("crypt_alphabet", ""), settings.get("normal_alphabet", "")


def generate_decryption_key(crypt_alphabet: str, normal_alphabet: str) -> dict:
    """
    generates decryption key
    Args:
        crypt_alphabet: str
        normal_alphabet: str
    """
    decryption_mapping = dict(zip(crypt_alphabet, normal_alphabet))
    return decryption_mapping


def frequency(input_file: str, output_file: str, settings_file: str, key_file: str) -> None:
    """
    decrypt text with settings and key, and writes the result to a file
    Args:
        input_file: str
        output_file: str
        settings_file: str
        key_file: str
    """
    crypt_alphabet, normal_alphabet = read_settings(settings_file)
    decryption_mapping = generate_decryption_key(crypt_alphabet, normal_alphabet)

    with open(input_file, 'r', encoding='UTF-8') as f:
        data = f.read().lower()
        data = data.replace('\n', '')

    decrypted_text = decrypt(data, decryption_mapping)
    with open(output_file, 'w', encoding='UTF-8') as decrypted_file:
        decrypted_file.write(decrypted_text)

    write_decryption_key(key_file, decryption_mapping)


def decrypt(text: str, decryption_mapping: dict) -> str:
    """
    Decrypt text
    Args:
        text: str
        decryption_mapping: dict
    """
    decrypted_text = ''
    for char in text:
        decrypted_text += decryption_mapping.get(char, char)
    return decrypted_text


def write_decryption_key(key_file_path: str, decryption_mapping: dict) -> None:
    """
    writes decryption key to a JSON file.
    Args:
        key_file_path: str
        decryption_mapping: dict
    """
    with open(key_file_path, 'w', encoding='UTF-8') as key_file:
        json.dump(decryption_mapping, key_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt text using provided settings and decryption key.')
    parser.add_argument('input_file', help='Path to the file containing encrypted text.')
    parser.add_argument('output_file', help='Path to write the decrypted text.')
    parser.add_argument('settings_file', help='Path to the JSON file containing encryption settings.')
    parser.add_argument('key_file', help='Path to the JSON file to write the decryption key.')
    args = parser.parse_args()

    frequency(args.input_file, args.output_file, args.settings_file, args.key_file)