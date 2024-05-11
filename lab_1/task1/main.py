import argparse
import json
from enum import Enum
import file_utils

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

class Mode(Enum):
    ENCRYPT = 1
    DECRYPT = 2

def caesar_cipher(text: str, step: int, mode: Mode) -> str:
    """
    Encrypt or decrypt text using Caesar cipher.
    
    Parameters:
    -----------
    text : str
        Text to encrypt or decrypt.
    step : int
        Step of encryption or decryption.
    mode : Mode
        Mode of operation, encrypt or decrypt.
        
    Returns:
    --------
    str
        Encrypted or decrypted text.
    """
    finish = ''
    for i in text:
        if i.upper() in alphabet:
            idx = alphabet.find(i.upper())
            if mode == Mode.ENCRYPT:
                idx2 = (idx + step) % len(alphabet)
            else:
                idx2 = (idx - step) % len(alphabet)
            finish += alphabet[idx2] if i.isupper() else alphabet[idx2].lower()
        else:
            finish += i
    return finish

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encrypt or decrypt text using Caesar cipher')
    parser.add_argument('file_path', type=str, help='Path to the file with text to process')
    parser.add_argument('step', type=int, help='Step of encryption or decryption')
    parser.add_argument('mode', type=str, choices=['encrypt', 'decrypt'], help='Mode of operation, encrypt or decrypt')
    args = parser.parse_args()

    text = file_utils.read_file(args.file_path)
    mode = Mode.ENCRYPT if args.mode == 'encrypt' else Mode.DECRYPT

    processed_text = caesar_cipher(text, args.step, mode)
    
    if args.mode == 'encrypt':
        file_utils.write_text_to_file('encrypted.txt', processed_text)
        file_utils.write_dict_to_json('key.json', {'step': args.step})
        print("Text encrypted successfully.")
    else:
        file_utils.write_text_to_file('decrypted.txt', processed_text)
        print("Text decrypted successfully.")
