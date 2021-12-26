

dump = bytes.fromhex("37a12aa3bd3322ba2f3c98aab92f39a41833aa9a2f3918b3243aaf18991c1cb119b1981b3e59aea6")

endiannes = 'little'


def rol(word, i):
    n = int.from_bytes(word, endiannes, signed=False)
    n = (n >> (len(word) * 8 - i)) | ((n << i) % 2 ** (len(word) * 8))
    return bytearray(n.to_bytes(len(word), endiannes, signed=False))


def ror(dword, i):
    n = int.from_bytes(dword, 'little', signed=False)
    n = ((n << (len(dword) * 8 - i)) % 2 ** (len(dword) * 8)) | (n >> i)
    return bytearray(n.to_bytes(len(dword), endiannes, signed=False))


def reverse(s):
    for i in range(len(s) - 4, -1, -1):
        dword = s[i:i + 4]
        dword = ror(dword, 7)
        s[i:i + 4] = dword

        word = s[i:i + 2]
        word = rol(word, 9)
        s[i:i + 2] = word

        byte = s[i]
        byte = byte ^ 0x4c
        s[i] = byte

    return s


def encrypt(s):
    for i in range(len(s) - 3):
        byte = s[i]
        byte = byte ^ 0x4c
        s[i] = byte

        word = s[i:i + 2]
        word = ror(word, 9)
        s[i:i + 2] = word

        dword = s[i:i + 4]
        dword = rol(dword, 7)
        s[i:i + 4] = dword

    return s


print(encrypt(bytearray('picoCTF{gEt_y0Ur_sH1fT5_r1gHt_0389c2b16}', encoding='ascii')).hex())
print(reverse(bytearray(dump)).decode('ascii'))
