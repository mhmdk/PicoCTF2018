import socket
import time
import threading
from random import randint

block_size = 16
starting_block = 7
start_index = starting_block * block_size
flag = bytearray(64 * b"x")

# payload = 30 * "a"
# m = """Agent,
# Greetings. My situation report is as follows:
# {0}
# My agent identifying code is: {1}.
# Down with the Soviets,
# 006
# """.format(payload, flag)

alpha = '0123456789abcdef'
host = ('2018shell.picoctf.com', 14263)


def recvuntil(delim,soc):
    ans = b''
    buf = soc.recv(4096)
    ans += buf
    # print(ans)
    if ans == b'':
        raise Exception
    while ans.find(delim) < 0:
        buf = soc.recv(4096)
        ans += buf
    return ans


def encrypt(report, anything,soc):
    soc.sendall(b'e\n')
    recvuntil(b'report: ',soc)
    soc.sendall(report + b"\n")
    recvuntil(b'else? ',soc)
    soc.sendall(anything + b"\n")
    cypher = recvuntil(b'(S)\n',soc)
    cypher = cypher.split(b"\n")[0]
    cypher = cypher.split(b': ')[1]
    # print(cypher)
    return bytearray(cypher)


def decrypt(cypher,soc):
    soc.sendall(b's\n')
    recvuntil(b'message: ',soc)
    soc.sendall(cypher + b"\n")
    cypher = recvuntil(b'(S)\n',soc)
    # print(cypher)
    return cypher.find(b'Successful decryption') >= 0


def solve(charnum):
    soc = socket.socket()
    soc.connect(host)
    recvuntil(b'(S)\n',soc)
    solved = False
    blocnum = charnum // block_size
    subindex = charnum % block_size
    report = bytearray(b"0" * 14 + b"0" * (block_size - subindex))
    anything = bytearray(b"0" * subindex)
    while not solved:
        try:
            newchar = randint(0, 255)
            if newchar != ord('\n'):
                report[randint(0, 15)] = newchar
            cypher = encrypt(report, anything,soc)
            cypher[-32:] = cypher[blocnum * 32:blocnum * 32 + 32]
            solved = decrypt(cypher,soc)
        except:
            soc.close()
            time.sleep(5)
            soc = socket.socket()
            soc.connect(host)
            print("new socket")
            recvuntil(b'(S)\n',soc)
            continue
    ans = cypher[-34:-32].decode('ascii')
    ans = int(ans, 16) ^ 16
    tmp = cypher[blocnum * 32 - 2: blocnum * 32].decode('ascii')
    ans = ans ^ int(tmp, 16)
    print(ans)
    return ans


def solve_and_assign(charnum):
    flag[charnum - start_index] = solve(charnum)
    print(f"solved character {charnum}")
    print(flag)


ts = []
for charnum in range(start_index + 3, start_index + 35, 1):
    ts.append(threading.Thread(target=solve_and_assign, name=str(charnum), args=(charnum,)))

for thread in ts:
    thread.start()

for thread in ts:
    thread.join()

print(flag)
