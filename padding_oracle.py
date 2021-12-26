import json
import socket


def send(iv, block):
    payload = iv.hex() + block.hex() + '\n'
    soc = socket.socket()
    soc.connect(("2018shell.picoctf.com", 6246))
    buf = soc.recv(4096)
    while buf.count(ord('?')) == 0:
        buf = soc.recv(4096)

    soc.send(bytes(payload, encoding="ascii"))

    buf = soc.recv(4096)
    ans = buf
    while len(buf) > 1:
        buf = soc.recv(4096)
        ans += buf

    return ans.decode('ascii')


def solve_block(block):
    iv = bytearray(b'\x00' * 16)
    ans = bytearray(16)
    for index in range(15, -1, -1):
        for i in range(15, index, -1):
            iv[i] = (16 - index) ^ ans[i]
        for i in range(256):
            iv[index] = i
            resp = send(iv, block)
            if resp.count('invalid padding') == 0:
                ans[index] = iv[index] ^ (16 - index)
                break
        print(ans)

    return ans


plaintext = bytearray('{"username":"guest","is_admin":"true","expires":"2020-11-11"}\x03\x03\x03', encoding='ascii')
iv = bytearray("a" * 16, encoding='ascii')

ciphertext = bytearray(64)
ans = bytearray(64)

for block_num in range(3, 0, -1):
    print("solving block {}".format(block_num))
    start_index = block_num * 16
    end_index = start_index + 16
    ciphertext[start_index: end_index] = solve_block(ans[start_index: end_index])
    for i in range(start_index, end_index):
        ans[i - 16] = ciphertext[i] ^ plaintext[i]

block_num = 0
start_index = block_num * 16
end_index = start_index + 16
ciphertext[start_index: end_index] = solve_block(ans[start_index: end_index])
for i in range(start_index, end_index):
    iv[i] = ciphertext[i] ^ plaintext[i]

flag = send(iv, ans)
print(flag)
