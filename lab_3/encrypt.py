import argparse
import os

from typing import Tuple
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_symmetric_key(sym_key_enc_path: str, private_key_path: str) -> bytes:
    """
    Расшифровать симметричный ключ с использованием закрытого ключа ассиметричного алгоритма.

    Аргументы:
        sym_key_enc_path (str): Путь к зашифрованному симметричному ключу.
        private_key_path (str): Путь к закрытому ключу ассиметричного алгоритма.

    Возвращает:
        bytes: Расшифрованный симметричный ключ.
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
    return sym_key


def encrypt_text(sym_key: bytes, plaintext_path: str, encrypted_text_path: str) -> None:
    """
    Зашифровать текст симметричным алгоритмом и сохранить в файл.

    Аргументы:
        sym_key (bytes): Симметричный ключ для шифрования.
        plaintext_path (str): Путь к шифруемому текстовому файлу.
        encrypted_text_path (str): Путь для сохранения зашифрованного текстового файла.

    Возвращает:
        None
    """
    with open(plaintext_path, 'rb') as f:
        plaintext = f.read()

    nonce = os.urandom(12)
    cipher = Cipher(algorithms.ChaCha20(sym_key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(encrypted_text_path, 'wb') as f:
        f.write(nonce + ciphertext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Шифрование данных гибридной системой')
    parser.add_argument('plaintext_path', help='Путь к шифруемому текстовому файлу')
    parser.add_argument('private_key_path', help='Путь к закрытому ключу ассиметричного алгоритма')
    parser.add_argument('sym_key_enc_path', help='Путь к зашированному ключу симметричного алгоритма')
    parser.add_argument('encrypted_text_path', help='Путь для сохранения зашифрованного текстового файла')
    args = parser.parse_args()

    sym_key = decrypt_symmetric_key(args.sym_key_enc_path, args.private_key_path)
    encrypt_text(sym_key, args.plaintext_path, args.encrypted_text_path)