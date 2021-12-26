import base64

path = "/home/muhammad/Downloads/pico2018-special-logo.bmp"

f = open(path, 'rb')

buf = f.read()

CHAR_SIZE = 8
for j in range(0x100):
    ans = bytearray(b"\x00"*(len(buf)//8 + 1))
    char_index = 0
    bit_index = 0

    for b in buf[j:0x200]:
        bit = 0
        if int(b) & 0x01 == 1:
            bit = 1
        if bit_index == CHAR_SIZE:
            bit_index = 0
            char_index += 1
        if bit_index > -1 and bit > 0:
            ans[char_index] |= 1 << (CHAR_SIZE - 1 - bit_index)
        bit_index += 1

    #print(base64.b64decode(ans))

    #print(ans.decode('ascii'))
    print((ans.find(b'picoCTF')))
    if ans.find(b'picoCTF') >=0:
        print(ans.decode('ascii'))
        break
f.close()