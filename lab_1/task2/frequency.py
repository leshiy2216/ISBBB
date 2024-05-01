def frequency():
    normal_alphabet = "ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"
    crypt_alphabet = "сах8мrло2bкедбр74t<1фу5>ч?ипайьы"

    decryption_mapping = dict(zip(crypt_alphabet, normal_alphabet))

    with open('cod3.txt', 'r', encoding='UTF-8') as f:
        data = f.read().lower()
        data = data.replace('\n', '')

    decrypted_text = decrypt(data, decryption_mapping)
    with open('decrypted_text.txt', 'w', encoding='UTF-8') as decrypted_file:
        decrypted_file.write(decrypted_text)


def decrypt(text, decryption_mapping):
    decrypted_text = ''
    for char in text:
        decrypted_text += decryption_mapping.get(char, char)

    return decrypted_text


frequency()