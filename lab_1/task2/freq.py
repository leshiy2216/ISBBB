import argparse

from collections import Counter
from task1.file_utils import save_to_json, save_to_text, read_file


def frequency(filename: str) -> None:
    """
    Вычисляет частоту встречаемости символов в текстовом файле и сохраняет результаты в JSON и текстовый файлы.
    
    Parameters
    ----------
    filename : str
        Имя входного текстового файла.
        
    Returns
    -------
    None
    """
    freq = {}
    data = read_file(filename).lower().replace('\n', '')
    
    freq = Counter(data)
    total_chars = len(data)
    freq_percentage = {char: count/total_chars for char, count in freq.items()}
    sorted_freq = sorted(freq_percentage.items(), key=lambda x: x[1], reverse=True)
    
    sorted_freq_text = [f"{char}: {frequency}" for char, frequency in sorted_freq]
    
    save_to_json(dict(sorted_freq), f'{filename}_frequencies.json')
    save_to_text(sorted_freq_text, f'{filename}_frequencies.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate character frequencies in a text file.')
    parser.add_argument('filename', type=str, help='Input text file name')
    args = parser.parse_args()
    
    frequency(args.filename)