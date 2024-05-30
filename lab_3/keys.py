import argparse
import os

from typing import Tuple
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_symmetric_key(sym_key_path: str) -> bytes:
    """
    Генерация симметричного ключа и его сериализация.

    Аргументы:
        sym_key_path (str): Путь для сериализации симметричного ключа.

    Возвращает:
        bytes: Сгенерированный симметричный ключ.
    """
    sym_key = os.urandom(32)
    with open(sym_key_path, 'wb') as f:
        f.write(sym_key)
    return sym_key


def generate_rsa_keys(public_key_path: str, private_key_path: str) -> Tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
    """
    Генерация открытого и закрытого ключей RSA и их сериализация.

    Аргументы:
        public_key_path (str): Путь для сериализации открытого ключа.
        private_key_path (str): Путь для сериализации закрытого ключа.

    Возвращает:
        Tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]: Сгенерированный открытый и закрытый ключи RSA.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    return public_key, private_key


def encrypt_symmetric_key(sym_key: bytes, public_key: rsa.RSAPublicKey, sym_key_enc_path: str) -> None:
    """
    Зашифрование симметричного ключа с использованием открытого ключа RSA и его сериализация.

    Аргументы:
        sym_key (bytes): Симметричный ключ для шифрования.
        public_key (rsa.RSAPublicKey): Открытый ключ RSA для шифрования.
        sym_key_enc_path (str): Путь для сериализации зашифрованного симметричного ключа.

    Возвращает:
        None
    """
    encrypted_sym_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    with open(sym_key_enc_path, 'wb') as f:
        f.write(encrypted_sym_key)


def generate_random_nonce(random_nonce_path: str) -> bytes:
    """
    Генерация случайного одноразового числа и его сериализация.

    Аргументы:
        random_nonce_path (str): Путь для сериализации случайного одноразового числа.

    Возвращает:
        bytes: Сгенерированное случайное одноразовое число.
    """
    random_nonce = os.urandom(16)  # 128 бит
    with open(random_nonce_path, 'wb') as f:
        f.write(random_nonce)
    return random_nonce


def serialize_random_nonce(random_nonce: bytes, random_nonce_path: str) -> None:
    """
    Сериализация случайного одноразового числа.

    Аргументы:
        random_nonce (bytes): Случайное одноразовое число для сериализации.
        random_nonce_path (str): Путь для сериализации случайного одноразового числа.

    Возвращает:
        None
    """
    with open(random_nonce_path, 'wb') as f:
        f.write(random_nonce)


def deserialize_random_nonce(random_nonce_path: str) -> bytes:
    """
    Десериализация случайного одноразового числа.

    Аргументы:
        random_nonce_path (str): Путь для десериализации случайного одноразового числа.

    Возвращает:
        bytes: Десериализованное случайное одноразовое число.
    """
    with open(random_nonce_path, 'rb') as f:
        random_nonce = f.read()
    return random_nonce


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Генерация ключей гибридной системы шифрования')
    parser.add_argument('sym_key_path', help='Путь для сериализации симметричного ключа')
    parser.add_argument('public_key_path', help='Путь для сериализации открытого ключа')
    parser.add_argument('private_key_path', help='Путь для сериализации закрытого ключа')
    parser.add_argument('random_nonce_path', help='Путь для сериализации случайного одноразового числа')
    args = parser.parse_args()

    sym_key = generate_symmetric_key(args.sym_key_path)
    public_key, private_key = generate_rsa_keys(args.public_key_path, args.private_key_path)