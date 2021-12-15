import struct


def bytes_to_int(byte: bytes=b"") -> int:
    result = 0
    for b in byte:
        result = result * 256 + int(b)
    return result

def decoder(name, out, search) -> None:
    file = open(name, "rb")
    input = file.read()
    b = bytearray()
    i = 0

    while i < len(input):
        offset_and_length, char = struct.unpack(">Hc", input[i:i+3])
        offset = offset_and_length >> 6
        length = offset_and_length - (offset << 6)
        i += 3
        if(offset == 0) and (length == 0):
            b.append(bytes_to_int(char))
        else:
            iterator = len(b) - search
            if iterator < 0:
                iterator = offset
            else:
                iterator += offset
            for pointer in range(length):
                b.append(b[iterator+pointer])
            b.append(bytes_to_int(char))
                
                            
    out.write(b)
    file.close()


max_offset = int(1024)
file = open("decoded.txt", "wb")
decoder("binary", file, max_offset)
file.close()

