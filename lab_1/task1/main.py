import argparse
import json


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def read_file(file_path: str) -> str:
    """
    the function read file
    Parameters
    ----------
    file_path : str

    Return
    ------
    str
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().upper()


def write_encrypted_text(text: str) -> None:
    """
    write encrypted text
    Parameters
    ----------
    text : str
    """
    with open('encrypted.txt', 'w', encoding='utf-8') as f:
        f.write(text)


def write_key(step: int) -> None:
    """
    write step to json

    Parameters
    ----------
    step : int
    """
    with open('key.json', 'w', encoding='utf-8') as f:
        json.dump({'step': step}, f)


def encryption(file_path: str, step: int) -> None:
    """
    encrypt text using Caesar cipher.

    Parameters
    ----------
    file_path : str
    step : int
    """
    content_upper = read_file(file_path)
        
    finish = ''
    for i in content_upper:
        idx = alphabet.find(i)
        idx2 = (idx + step) % len(alphabet)
        if i in alphabet:
            finish += alphabet[idx2]
        else:
            finish += i
            
    write_encrypted_text(finish)
    write_key(step)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='encrypt text using Caesar cipher')
    parser.add_argument('file_path', type=str, help='path to the file with text to encrypt him')
    parser.add_argument('step', type=int, help='step of encryption')
    args = parser.parse_args()
    
    encryption(args.file_path, args.step)
