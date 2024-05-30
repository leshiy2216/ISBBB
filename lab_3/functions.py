import os
from typing import Union
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def generate_key_pair() -> rsa.RSAPrivateKey:
    """
    Генерирует пару RSA ключей.

    Returns:
        rsa.RSAPrivateKey: Сгенерированный RSA закрытый ключ.
    """
    try:
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)
    except Exception as ex:
        raise Exception(f"Ошибка генерации ключа: {ex}")


def encrypt_symmetric_key(private_key: rsa.RSAPrivateKey, symmetric_key: bytes) -> bytes:
    """
    Шифрует симметричный ключ с использованием RSA.

    Args:
        private_key (rsa.RSAPrivateKey): RSA закрытый ключ, используемый для шифрования.
        symmetric_key (bytes): Симметричный ключ для шифрования.

    Returns:
        bytes: Зашифрованный симметричный ключ.
    """
    try:
        return private_key.public_key().encrypt(
            symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as ex:
        raise Exception(f"Ошибка шифрования симметричного ключа: {ex}")


def decrypt_symmetric_key(private_key: rsa.RSAPrivateKey, encrypted_symmetric_key: bytes) -> bytes:
    """
    Расшифровывает зашифрованный симметричный ключ с использованием RSA.

    Args:
        private_key (rsa.RSAPrivateKey): RSA закрытый ключ, используемый для расшифровки.
        encrypted_symmetric_key (bytes): Зашифрованный симметричный ключ для расшифровки.

    Returns:
        bytes: Расшифрованный симметричный ключ.
    """
    try:
        return private_key.decrypt(
            encrypted_symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as ex:
        raise Exception(f"Ошибка расшифровки симметричного ключа: {ex}")
    

def serialize_private_key(private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Сериализует закрытый ключ в формате PEM.

    Args:
        private_key (rsa.RSAPrivateKey): Закрытый ключ для сериализации.

    Returns:
        bytes: Сериализованный закрытый ключ в формате PEM.
    """
    try:
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    except Exception as ex:
        raise Exception(f"Ошибка сериализации закрытого ключа: {ex}")


def serialize_public_key(public_key: rsa.RSAPublicKey) -> bytes:
    """
    Сериализует открытый ключ в формате PEM.

    Args:
        public_key (rsa.RSAPublicKey): Открытый ключ для сериализации.

    Returns:
        bytes: Сериализованный открытый ключ в формате PEM.
    """
    try:
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    except Exception as ex:
        raise Exception(f"Ошибка сериализации открытого ключа: {ex}")

  
def load_private_key(private_key_bytes: bytes) -> rsa.RSAPrivateKey:
    """
    Загружает закрытый ключ из его байтового представления.

    Args:
        private_key_bytes (bytes): Байтовое представление закрытого ключа.

    Returns:
        rsa.RSAPrivateKey: Загруженный закрытый ключ.
    """
    try:
        return serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())
    except Exception as ex:
        raise Exception(f"Ошибка загрузки закрытого ключа: {ex}")
    

def generate_keys(private_key_path: str, public_key_path: str, symmetric_key_path: str) -> None:
    """
    Генерирует пару ключей для асимметричного шифрования и симметричный ключ для гибридного шифрования.

    Args:
        private_key_path (str): Путь для сохранения закрытого ключа.
        public_key_path (str): Путь для сохранения открытого ключа.
        symmetric_key_path (str): Путь для сохранения симметричного ключа.
    """
    try:
        private_key = generate_key_pair()
        public_key = private_key.public_key()
        symmetric_key = os.urandom(32)
        with open(public_key_path, "wb") as f:
            f.write(serialize_public_key(public_key))
        with open(private_key_path, "wb") as f:
            f.write(serialize_private_key(private_key))
        with open(symmetric_key_path, "wb") as f:
            f.write(symmetric_key)
    except Exception as ex:
        raise Exception(f"Ошибка генерации ключей: {ex}")


def encrypt_file(initial_file_path: str, private_key_path: str, symmetric_key_path: str, encrypted_file_path: str) -> None:
    """
    Шифрует файл с использованием гибридного шифрования.

    Args:
        initial_file_path (str): Путь к файлу, который нужно зашифровать.
        private_key_path (str): Путь к закрытому ключу.
        symmetric_key_path (str): Путь к симметричному ключу.
        encrypted_file_path (str): Путь для сохранения зашифрованного файла.
    """
    try:
        private_key_bytes = open(private_key_path, "rb").read()
        private_key = load_private_key(private_key_bytes)
        symmetric_key = open(symmetric_key_path, "rb").read()
        encrypted_symmetric_key = encrypt_symmetric_key(private_key, symmetric_key)
        with open(symmetric_key_path, "wb") as f:
            f.write(encrypted_symmetric_key)
        with open(initial_file_path, "rb") as f_in, open(encrypted_file_path, "wb") as f_out:
            plaintext = f_in.read()
            ciphertext = encrypt_data(symmetric_key, plaintext)
            f_out.write(ciphertext)
    except Exception as ex:
        raise Exception(f"Ошибка шифрования файла: {ex}")


def decrypt_file(encrypted_file_path: str, private_key_path: str, symmetric_key_path: str, decrypted_file_path: str) -> None:
    """
    Дешифрует файл, зашифрованный с использованием гибридного шифрования.

    Args:
        encrypted_file_path (str): Путь к зашифрованному файлу.
        private_key_path (str): Путь к закрытому ключу.
        symmetric_key_path (str): Путь к симметричному ключу.
        decrypted_file_path (str): Путь для сохранения расшифрованного файла.
    """
    try:
        private_key_bytes = open(private_key_path, "rb").read()
        private_key = load_private_key(private_key_bytes)
        encrypted_symmetric_key = open(symmetric_key_path, "rb").read()
        symmetric_key = decrypt_symmetric_key(private_key, encrypted_symmetric_key)
        with open(encrypted_file_path, "rb") as f_in, open(decrypted_file_path, "wb") as f_out:
            iv = f_in.read(16)
            cipher = Cipher(algorithms.ChaCha20(symmetric_key, iv), mode=None)
            decryptor = cipher.decryptor()
            while chunk := f_in.read(128):
                decrypted_chunk = decryptor.update(chunk)
                f_out.write(decrypted_chunk)
            f_out.write(decryptor.finalize())
    except Exception as ex:
        raise Exception(f"Ошибка дешифрования файла: {ex}")
    

def encrypt_data(symmetric_key: bytes, plaintext: bytes) -> bytes:
    """
    Шифрует текст с использованием симметричного алгоритма шифрования ChaCha20.

    Args:
        symmetric_key (bytes): Симметричный ключ, используемый для шифрования.
        plaintext (bytes): Текст для шифрования.

    Returns:
        bytes: Зашифрованный текст, полученный в результате процесса шифрования.
    """
    try:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.ChaCha20(symmetric_key, iv), mode=None)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv + ciphertext
    except Exception as ex:
        raise Exception(f"Ошибка шифрования данных: {ex}")
    
    
def decrypt_data(symmetric_key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
    """
    Дешифрует зашифрованный текст с использованием симметричного алгоритма шифрования ChaCha20.

    Args:
        symmetric_key (bytes): Симметричный ключ, используемый для дешифрования.
        ciphertext (bytes): Зашифрованный текст для дешифрования.
        iv (bytes): Инициализационный вектор, использованный при шифровании.

    Returns:
        bytes: Расшифрованный текст.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(symmetric_key, iv), mode=None)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as ex:
        raise Exception(f"Ошибка дешифрования данных: {ex}")