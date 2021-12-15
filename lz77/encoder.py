import struct
import math

def encode(search, forward):
    if len(search) == 0:
        return 0, 0, forward[0]
    if len(forward) == 0:
        return -1, -1, ""

    best_length = 0
    best_offset = 0
    space = search + forward
    for i in range(0, len(search)):
        j = 0
        while space[i + j] == space[len(search) + j]:
            j = j + 1
            if len(search) + j == len(space):
                j -= 1
                break
            if i + j >= len(search):
                break
        if j > best_length:
            best_offset = i
            best_length = j

    return (best_offset, best_length, space[len(search) + best_length])

def int_to_bytes(number):
    hrepr = hex(number).replace('0x', '')
    if len(hrepr) % 2 == 1:
        hrepr = '0' + hrepr
    return bytes.fromhex(hrepr)

f = open('test.txt', "rb")
text = f.read()
f.close()

maxbites = 16
max_offset = int(1024)
max_length = int(math.pow(2, (maxbites - (math.log(max_offset, 2)))))

file = open("binary", "wb")
i = 0
j = 0

while j < len(text):
    search = text[i:j]
    forward = text[j:j + max_length]
    (offset, length, char) = encode(search, forward)
    shifted_offset = offset << 6
    offset_and_length = shifted_offset + length
    data = struct.pack(">Hc", offset_and_length, int_to_bytes(char))
    file.write(data)
    j = j + length + 1
    i = j - max_offset
    if i < 0:
        i = 0

file.close()
