def frequency():
    crypt_alphabet = "cа8r<4>хмелдбbр51к2оуф7t"
    normal_alphabet = " ОЕНЧЬГИТМСЛПЯВЭЙРКАЖЗДУ"

    decryption_mapping = dict(zip(crypt_alphabet, normal_alphabet))

    with open('cod3.txt', 'r', encoding='UTF-8') as f:
        data = f.read().lower()
        data = data.replace('\n', '')

    decrypted_text = decrypt(data, decryption_mapping)
    with open('result.txt', 'w', encoding='UTF-8') as decrypted_file:
        decrypted_file.write(decrypted_text)


def decrypt(text, decryption_mapping):
    decrypted_text = ''
    for char in text:
        decrypted_text += decryption_mapping.get(char, char)

    return decrypted_text


frequency()