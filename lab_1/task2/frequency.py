import argparse
import json
from typing import Tuple
from task1.file_utils import read_file, write_text_to_file, read_settings, write_decryption_key


def generate_decryption_key(crypt_alphabet: str, normal_alphabet: str) -> dict:
    """
    Generate decryption key.
    Args:
        crypt_alphabet: str
        normal_alphabet: str
    """
    decryption_mapping = dict(zip(crypt_alphabet, normal_alphabet))
    return decryption_mapping


def decrypt_text(input_file: str, output_file: str, settings_file: str, key_file: str) -> None:
    """
    Decrypt text with settings and key, and write the result to a file.
    Args:
        input_file (str): Path to the input file containing encrypted text.
        output_file (str): Path to write the decrypted text.
        settings_file (str): Path to the JSON file containing encryption settings.
        key_file (str): Path to the JSON file to write the decryption key.
    """
    crypt_alphabet, normal_alphabet = decryption_settings
    decryption_mapping = generate_decryption_key(crypt_alphabet, normal_alphabet)

    data = read_file(input_file).lower().replace('\n', '')

    decrypted_text = decrypt(data, decryption_mapping)
    write_text_to_file(output_file, decrypted_text)

    write_decryption_key(key_file, decryption_mapping)


def decrypt(text: str, decryption_mapping: dict) -> str:
    """
    Decrypt text.
    Args:
        text: str
        decryption_mapping: dict
    """
    decrypted_text = ''
    for char in text:
        decrypted_text += decryption_mapping.get(char, char)
    return decrypted_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt text using provided settings and decryption key.')
    parser.add_argument('input_file', help='Path to the file containing encrypted text.')
    parser.add_argument('output_file', help='Path to write the decrypted text.')
    parser.add_argument('settings_file', help='Path to the JSON file containing encryption settings.')
    parser.add_argument('key_file', help='Path to the JSON file to write the decryption key.')
    args = parser.parse_args()

    decryption_settings = read_settings(args.settings_file)
    
    decrypt_text(args.input_file, args.output_file, args.settings_file, args.key_file)