from collections import Counter
import json


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
    total_chars = len(data)
    for i in freq:
        freq[i] /= total_chars
    sorted_freq = Counter(freq).most_common()
    
    with open('frequencies.json', 'w') as json_file:
        json.dump(dict(sorted_freq), json_file, indent=4)
    
    with open('frequencies.txt', 'w', encoding='UTF-8') as text_file:
        for char, frequency in sorted_freq:
            text_file.write(f"{char}: {frequency}\n")


if __name__ == "__main__":
    frequency()