import collections


def frequency():
    f = open('cod3.txt', 'r', encoding='UTF-8')
    text = f.read()
    text = text.upper()
    leng = len(text)
    alphabetcrypt = dict()
    for i in text:
        alphabetcrypt[i] = text.count(i) / leng
    alphabetcrypt = dict(sorted(alphabetcrypt.items()))
    print(alphabetcrypt)
    replace_symbol(text, alphabetcrypt)

def replace_symbol(text, alphabetcrypt):
    alphabet = {1: 'О',
                2: 'И',
                3: 'Е',
                4: 'Т',
                5: 'А',
                6: 'С',
                7: 'Н',
                8: 'В',
                9: 'Р',
                10: 'Л',
                11: 'М',
                12: 'К',
                13: 'Д'}

frequency()