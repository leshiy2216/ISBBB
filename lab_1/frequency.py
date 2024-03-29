from collections import Counter
import json

RUS = ' оиеантсрвмлдякпзыьучжгхфйюбцшщэъ'


def frequency():
    freq = {}
    with open('cod3.txt', 'r', encoding='UTF-8') as f:
        data = f.read().lower()
        data = data.replace('\n', '')
        for char in data:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
    for i in freq:
        freq[i] /= len(data)
    sorted_freq = Counter(freq)
    decrypt(data, sorted_freq)


def decrypt(text, alphabet):
    text = text.replace('c', ' ')
    text = text.replace('a', 'о')
    text = text.replace('x', 'и')


if __name__ == "__main__":
    frequency()