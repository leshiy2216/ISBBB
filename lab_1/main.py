alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def encryption():
    f = open('unencrypted.txt', 'r', encoding='utf-8')
    content = f.read()
    content_upper = content.upper()
    finish =  ''
    step = int(input('Step: '))
    for i in content_upper:
        idx = alphabet.find(i)
        idx2 = (idx + step) % len(alphabet)
        if i in alphabet:
            finish += alphabet[idx2]
        else:
            finish += i
    with open('encrypted.txt', 'w', encoding='utf-8') as d:
        d.write(finish)
    with open('key.txt', 'w', encoding='utf-8') as e:
        e.write(str(step))


if __name__ == "__main__":
    encryption()