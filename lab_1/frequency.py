def frequency():
    f = open('cod3.txt', 'r', encoding='utf-8')
    content = f.read()
    content_upper = content.upper()

    
    freq = {}
    total = len(content_upper)
    for symbol in content_upper:
        if symbol in freq:
            freq[symbol] += 1
        else:
            freq[symbol] = 1
    for symbol, count in sorted(freq.items()):
        freq = count / total
        print(f"simvol: {symbol}, freq: {freq:.4f}")