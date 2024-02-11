alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


step = int(input('Step: '))
message = input('Message for schipher: ').upper()
finish =  ''


for i in message:
    idx = alphabet.find(i)
    idx2 = idx + step
    if i in alphabet:
        finish += alphabet[idx2]
    else:
        finish += i
print(finish)