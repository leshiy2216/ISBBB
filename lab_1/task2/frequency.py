from collections import Counter
import json


def frequency():
    freq_encrypted = {}
    with open('cryptALPHA.json', 'r', encoding='UTF-8') as encrypted_freq_file:
        freq_encrypted = json.load(encrypted_freq_file)

    freq_normal = {}
    with open('encryptSIGMA.json', 'r', encoding='UTF-8') as normal_freq_file:
        freq_normal = json.load(normal_freq_file)

    with open('cod3.txt', 'r', encoding='UTF-8') as f:
        data = f.read().lower()
        data = data.replace('\n', '')

    decrypted_text = decrypt(data, freq_encrypted, freq_normal)
    with open('decrypted_text2.txt', 'w', encoding='UTF-8') as decrypted_file:
        decrypted_file.write(decrypted_text)


def decrypt(text, freq_encrypted, freq_normal):
    sorted_freq_encrypted = Counter(freq_encrypted)
    sorted_freq_normal = Counter(freq_normal)

    encrypted_chars = sorted_freq_encrypted.keys()
    normal_chars = sorted_freq_normal.keys()

    decryption_mapping = {}
    for enc_char, norm_char in zip(encrypted_chars, normal_chars):
        decryption_mapping[enc_char] = norm_char

    decrypted_text = ''
    for char in text:
        if char in decryption_mapping:
            decrypted_text += decryption_mapping[char]
        else:
            decrypted_text += char

    return decrypted_text


frequency()