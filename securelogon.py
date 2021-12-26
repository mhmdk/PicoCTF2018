import json
import base64

payload = "{'username':'a','admin':0,'password':'ss'}"
data = {'username': 'a','admin': 0,'password': 'ss'}
data = json.dumps(data, sort_keys=True)
print(data)

st = json.loads(data)
print(st)

def flip_coockie(cooci):
    b = bytearray(base64.b64decode(cooci))
    b[10] ^= ord('0')
    b[10] ^= ord('1')

    return base64.b64encode(bytes(b)).decode('ascii')

cookie = "trZoSbfaBR4SjxC/suANpWRwxw37/CRoEbKMtuimrKoyTTF+WUTWk9LD1/CP0gzu6OSdhuvT5hfK7vXa4NtVqFfhejVqTQVddSYa78UAQkw="
cookie= flip_coockie(cookie)
print(cookie)