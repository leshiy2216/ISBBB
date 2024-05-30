import argparse
import os

from typing import Tuple
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_text(sym_key_enc_path: str, encrypted_text_path: str, private_key_path: str, decrypted_text_path: str) -> None:
    """
    Дешифровать текст симметричным алгоритмом и сохранить в файл.

    Аргументы:
        sym_key_enc_path (str): Путь к зашированному ключу симметричного алгоритма.
        encrypted_text_path (str): Путь к зашифрованному текстовому файлу.
        private_key_path (str): Путь к закрытому ключу ассиметричного алгоритма.
        decrypted_text_path (str): Путь для сохранения расшифрованного текстового файла.

    Возвращает:
        None
    """
    with open(sym_key_enc_path, 'rb') as f:
        encrypted_sym_key = f.read()
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    sym_key = private_key.decrypt(
        encrypted_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(encrypted_text_path, 'rb') as f:
        data = f.read()
    nonce = data[:12]
    ciphertext = data[12:]
    cipher = Cipher(algorithms.ChaCha20(sym_key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(decrypted_text_path, 'wb') as f:
        f.write(plaintext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Дешифрование данных гибридной системой')
    parser.add_argument('sym_key_enc_path', help='Путь к зашированному ключу симметричного алгоритма')
    parser.add_argument('encrypted_text_path', help='Путь к зашифрованному текстовому файлу')
    parser.add_argument('private_key_path', help='Путь к закрытому ключу ассиметричного алгоритма')
    parser.add_argument('decrypted_text_path', help='Путь для сохранения расшифрованного текстового файла')
    args = parser.parse_args()

    decrypt_text(args.sym_key_enc_path, args.encrypted_text_path, args.private_key_path, args.decrypted_text_path)