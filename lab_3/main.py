import argparse
import json
import os

from typing import Dict, Any
from functions import create_keys, secure_file, unsecure_file


def load_settings(filepath: str) -> Dict[str, Any]:
    """
    Загружает настройки из указанного файла.

    Args:
        filepath (str): Путь к файлу с настройками.

    Returns:
        Dict[str, Any]: Словарь с настройками.

    Raises:
        Exception: Если не удалось загрузить настройки.
    """
    try:
        with open(filepath) as json_file:
            return json.load(json_file)
    except Exception as e:
        raise Exception(f"Не удалось загрузить настройки из {filepath}: {e}")


def main() -> None:
    """
    Главная функция, управляющая режимами генерации ключей, шифрования и дешифрования.

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Гибридное шифрование с использованием асимметричных и симметричных ключей")
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-gen', '--generate', action='store_true', help='Генерация ключей')
    action_group.add_argument('-enc', '--encrypt', action='store_true', help='Шифрование файла')
    action_group.add_argument('-dec', '--decrypt', action='store_true', help='Дешифрование файла')
    args = parser.parse_args()

    settings = load_settings('settings.json')

    if args.generate:
        create_keys(settings['private_key'], settings['public_key'], settings['symmetric_key'])
    elif args.encrypt:
        secure_file(settings['input_file'], settings['private_key'], settings['symmetric_key'], settings['encrypted_output'])
    elif args.decrypt:
        unsecure_file(settings['encrypted_output'], settings['private_key'], settings['symmetric_key'], settings['decrypted_output'])


if __name__ == "__main__":
    main()